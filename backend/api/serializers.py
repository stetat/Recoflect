from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import BudgetPeriod, Category, Family, FamilyJoinRequest, Goal, Record

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["role"] = self.user.role
        data["user_id"] = self.user.id
        data["first_name"] = self.user.first_name

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "role", "family"]
        depth = 1


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "role", "family"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class RecordSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["category"].queryset = Category.objects.filter(
                user=request.user
            )

    class Meta:
        model = Record
        fields = [
            "id",
            "type",
            "category",
            "category_title",
            "amount",
            "date",
            "reflection",
        ]


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id",
            "title",
            "amount",
            "current_amount",
            "deadline",
            "importance",
        ]

    def validate_title(self, value):
        queryset = Goal.objects.filter(title=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Goal with this title already exists.")
        return value

    def validate(self, attrs):
        amount = attrs.get("amount", getattr(self.instance, "amount", None))
        current_amount = attrs.get(
            "current_amount", getattr(self.instance, "current_amount", 0)
        )

        if amount is not None and amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0."})

        if current_amount is not None and current_amount < 0:
            raise serializers.ValidationError(
                {"current_amount": "Current amount cannot be negative."}
            )

        if (
            amount is not None
            and current_amount is not None
            and current_amount > amount
        ):
            raise serializers.ValidationError(
                {"current_amount": "Current amount cannot be greater than target amount."}
            )

        return attrs


class FamilyMemberSerializer(serializers.ModelSerializer):
    weekly_income = serializers.SerializerMethodField()
    weekly_expense = serializers.SerializerMethodField()
    limit = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "role",
            "weekly_income",
            "weekly_expense",
            "limit",
        ]

    def _get_week_range(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    def _get_week_sum(self, obj, record_type):
        start_of_week, end_of_week = self._get_week_range()
        total = (
            Record.objects.filter(
                category__user=obj,
                type=record_type,
                date__range=(start_of_week, end_of_week),
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return int(total)

    def get_weekly_income(self, obj):
        return self._get_week_sum(obj, Record.Type.INCOME)

    def get_weekly_expense(self, obj):
        return self._get_week_sum(obj, Record.Type.EXPENSE)

    def get_limit(self, obj):
        budget_period = (
            BudgetPeriod.objects.filter(user=obj).order_by("-end_date", "-start_date").first()
        )
        return budget_period.limit_amount if budget_period else None


class FamilySerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True, read_only=True)
    current_user_role = serializers.SerializerMethodField()
    current_user_id = serializers.SerializerMethodField()
    join_requests = serializers.SerializerMethodField()

    class Meta:
        model = Family
        fields = [
            "id",
            "family_name",
            "invite_code",
            "members",
            "current_user_role",
            "current_user_id",
            "join_requests",
        ]

    def get_current_user_role(self, obj):
        request = self.context.get("request")
        return getattr(request.user, "role", None) if request else None

    def get_current_user_id(self, obj):
        request = self.context.get("request")
        return str(request.user.id) if request else None

    def get_join_requests(self, obj):
        return FamilyJoinRequestSerializer(
            obj.join_requests.filter(status=FamilyJoinRequest.Status.PENDING),
            many=True,
            context=self.context,
        ).data


class FamilyCreateSerializer(serializers.Serializer):
    family_name = serializers.CharField(max_length=100)


class FamilyJoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)
    desired_role = serializers.ChoiceField(choices=User.Role.choices)


class FamilyJoinRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = FamilyJoinRequest
        fields = [
            "id",
            "username",
            "first_name",
            "desired_role",
            "status",
            "created_at",
        ]


class FamilyPendingResponseSerializer(serializers.Serializer):
    family = FamilySerializer(allow_null=True)
    pending_join_request = FamilyJoinRequestSerializer(allow_null=True)
