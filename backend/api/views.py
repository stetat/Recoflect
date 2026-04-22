from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    BudgetPeriod,
    Category,
    Family,
    FamilyJoinRequest,
    Goal,
    Record,
    User,
    ai_abstract,
    groq_ai,
)
from .serializers import (
    CategorySerializer,
    CustomTokenObtainPairSerializer,
    FamilyCreateSerializer,
    FamilyJoinRequestSerializer,
    FamilyJoinSerializer,
    FamilySerializer,
    GoalSerializer,
    RecordSerializer,
    RegisterSerializer,
)
from .utils import generate_family_invite_code

User = get_user_model()
ai_bot: ai_abstract = groq_ai()


def serialize_family(family, request):
    return FamilySerializer(family, context={"request": request}).data


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response({"error": "Invalid token or already blacklisted"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def advice_view(request):
    prompt_text = str(request.data.get("prompt", "")).strip()
    if not prompt_text:
        return Response(
            {"detail": "Prompt is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        advice = ai_bot.prompt(prompt_text)
    except ValueError as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response({"advice": advice}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def budget_view(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    def get_actual_spent():
        return int(
            Record.objects.filter(
                user=request.user,
                type=Record.Type.EXPENSE,
                date__range=(start_of_week, end_of_week),
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

    def build_response(budget):
        actual_spent = get_actual_spent()
        percent_used = (
            round(actual_spent / budget.limit_amount * 100, 1)
            if budget.limit_amount
            else 0
        )
        return Response(
            {
                "limit_amount": budget.limit_amount,
                "actual_spent": actual_spent,
                "percent_used": min(percent_used, 100),
            }
        )

    if request.method == "GET":
        budget = BudgetPeriod.objects.filter(
            user=request.user,
            start_date=start_of_week,
            end_date=end_of_week,
        ).first()
        if not budget:
            return Response(
                {
                    "limit_amount": None,
                    "actual_spent": get_actual_spent(),
                    "percent_used": 0,
                }
            )
        return build_response(budget)

    limit_amount = request.data.get("limit_amount")
    try:
        limit_amount = int(limit_amount)
        if limit_amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return Response(
            {"detail": "limit_amount must be a positive integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    budget_qs = BudgetPeriod.objects.filter(
        user=request.user,
        start_date=start_of_week,
        end_date=end_of_week,
    )
    if budget_qs.exists():
        budget_qs.update(limit_amount=limit_amount)
        budget = budget_qs.first()
    else:
        budget = BudgetPeriod.objects.create(
            user=request.user,
            start_date=start_of_week,
            end_date=end_of_week,
            limit_amount=limit_amount,
            actual_spent=0,
        )
    return build_response(budget)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(Q(user=self.request.user) | Q(user__isnull=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def summary(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        user_records = request.user.records.filter(
            date__range=[start_of_week, end_of_week]
        )

        income_total = (
            user_records.income().aggregate(Sum("amount"))["amount__sum"] or 0
        )
        expense_total = (
            user_records.expenses().aggregate(Sum("amount"))["amount__sum"] or 0
        )
        net = income_total - expense_total

        return Response(
            {
                "income": income_total,
                "expense": expense_total,
                "net": net,
                "period": {"start": start_of_week, "end": end_of_week},
            }
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = Record.objects.filter(user=self.request.user).order_by("-date")
        record_type = self.request.query_params.get("type")
        reflection = self.request.query_params.get("reflection")
        if record_type:
            qs = qs.filter(type=record_type)
        if reflection:
            qs = qs.filter(reflection=reflection)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Goal.objects.filter(user=self.request.user).order_by(
            "deadline", "title"
        )

        importance = self.request.query_params.get("importance")
        overdue = self.request.query_params.get("overdue")

        if importance:
            queryset = queryset.filter(importance=importance)
        if overdue == "true":
            queryset = queryset.filter(deadline__lt=timezone.now().date())

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def family_detail_view(request):
    if request.user.family is None:
        pending_request = (
            FamilyJoinRequest.objects.filter(
                user=request.user, status=FamilyJoinRequest.Status.PENDING
            )
            .select_related("user", "family")
            .first()
        )
        payload = {
            "family": None,
            "pending_join_request": FamilyJoinRequestSerializer(
                pending_request, context={"request": request}
            ).data
            if pending_request
            else None,
        }
        return Response(payload, status=status.HTTP_200_OK)

    return Response(
        serialize_family(request.user.family, request), status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_create_view(request):
    if request.user.family is not None:
        return Response(
            {"detail": "You are already in a family."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = FamilyCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        family = Family.objects.create(
            family_name=serializer.validated_data["family_name"].strip()
        )
        request.user.family = family
        request.user.role = User.Role.PARENT
        request.user.save(update_fields=["family", "role"])

    return Response(serialize_family(family, request), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_join_view(request):
    if request.user.family is not None:
        return Response(
            {"detail": "Leave your current family before joining another one."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = FamilyJoinSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    invite_code = serializer.validated_data["invite_code"].strip().upper()
    desired_role = int(serializer.validated_data["desired_role"])

    if desired_role not in (User.Role.PARENT, User.Role.CHILD):
        return Response(
            {"desired_role": ["Choose Parent or Child."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        family = Family.objects.get(invite_code=invite_code)
    except Family.DoesNotExist:
        return Response(
            {"invite_code": ["Family with this invite code was not found."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if FamilyJoinRequest.objects.filter(
        user=request.user, status=FamilyJoinRequest.Status.PENDING
    ).exists():
        return Response(
            {"detail": "You already have a pending family request."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    join_request = FamilyJoinRequest.objects.create(
        family=family,
        user=request.user,
        desired_role=desired_role,
    )

    return Response(
        {
            "detail": "Request sent to family admin.",
            "pending_join_request": FamilyJoinRequestSerializer(
                join_request, context={"request": request}
            ).data,
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_regenerate_invite_view(request):
    family = request.user.family
    if family is None:
        return Response(
            {"detail": "You are not in a family."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if request.user.role != User.Role.PARENT:
        return Response(
            {"detail": "Only parents can regenerate the invite code."},
            status=status.HTTP_403_FORBIDDEN,
        )

    family.invite_code = generate_family_invite_code()
    family.save(update_fields=["invite_code"])

    return Response(serialize_family(family, request), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_remove_member_view(request):
    family = request.user.family
    member_id = request.data.get("member_id")

    if family is None:
        return Response(
            {"detail": "You are not in a family."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if request.user.role != User.Role.PARENT:
        return Response(
            {"detail": "Only parents can remove members."},
            status=status.HTTP_403_FORBIDDEN,
        )
    if not member_id:
        return Response(
            {"member_id": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        member = family.members.get(pk=member_id)
    except User.DoesNotExist:
        return Response(
            {"detail": "Member not found in your family."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if member.pk == request.user.pk:
        return Response(
            {"detail": "Use leave family instead of removing yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if (
        member.role == User.Role.PARENT
        and family.members.parents().count() == 1
        and family.members.count() > 1
    ):
        return Response(
            {
                "detail": "You cannot remove the last parent while family members still remain."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    member.family = None
    member.role = User.Role.NONE
    member.save(update_fields=["family", "role"])

    return Response(serialize_family(family, request), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_leave_view(request):
    family = request.user.family
    if family is None:
        return Response(
            {"detail": "You are not in a family."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if (
        request.user.role == User.Role.PARENT
        and family.members.parents().count() == 1
        and family.members.count() > 1
    ):
        return Response(
            {
                "detail": "You cannot leave as the last parent while other members remain."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        request.user.family = None
        request.user.role = User.Role.NONE
        request.user.save(update_fields=["family", "role"])

        if not family.members.exists():
            family.delete()

    return Response({"family": None}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_request_approve_view(request, request_id):
    family = request.user.family
    if family is None or request.user.role != User.Role.PARENT:
        return Response(
            {"detail": "Only parents in a family can approve requests."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        join_request = family.join_requests.select_related("user").get(
            pk=request_id, status=FamilyJoinRequest.Status.PENDING
        )
    except FamilyJoinRequest.DoesNotExist:
        return Response(
            {"detail": "Request not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    with transaction.atomic():
        join_request.status = FamilyJoinRequest.Status.APPROVED
        join_request.save(update_fields=["status"])
        join_request.user.family = family
        join_request.user.role = join_request.desired_role
        join_request.user.save(update_fields=["family", "role"])

    return Response(serialize_family(family, request), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def family_request_reject_view(request, request_id):
    family = request.user.family
    if family is None or request.user.role != User.Role.PARENT:
        return Response(
            {"detail": "Only parents in a family can reject requests."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        join_request = family.join_requests.get(
            pk=request_id, status=FamilyJoinRequest.Status.PENDING
        )
    except FamilyJoinRequest.DoesNotExist:
        return Response(
            {"detail": "Request not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    join_request.status = FamilyJoinRequest.Status.REJECTED
    join_request.save(update_fields=["status"])

    return Response(serialize_family(family, request), status=status.HTTP_200_OK)
