from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Category, Goal, Record

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
