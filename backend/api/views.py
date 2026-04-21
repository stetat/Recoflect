from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, Goal, Record
from .serializers import (
    CategorySerializer,
    CustomTokenObtainPairSerializer,
    GoalSerializer,
    RecordSerializer,
    RegisterSerializer,
)

User = get_user_model()


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
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Record.objects.filter(category__user=self.request.user).order_by("-date")
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
        queryset = Goal.objects.filter(user=self.request.user).order_by("deadline", "title")

        importance = self.request.query_params.get("importance")
        overdue = self.request.query_params.get("overdue")

        if importance:
            queryset = queryset.filter(importance=importance)
        if overdue == "true":
            queryset = queryset.filter(deadline__lt=timezone.now().date())

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
