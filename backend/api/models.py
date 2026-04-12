import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_family_invite_code


class User(AbstractUser):
    class Role(models.IntegerChoices):
        PARENT = 1, "Parent"
        CHILD = 2, "Child"
        NONE = 3, "None"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField()
    role = models.IntegerField(choices=Role, default=Role.NONE)
    family = models.ForeignKey(
        "Family",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    def __str__(self):
        return self.username


class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    family_name = models.CharField(max_length=100)
    invite_code = models.CharField(
        max_length=6, unique=True, default=generate_family_invite_code
    )

    def __str__(self):
        return self.family_name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=60, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")


class Record(models.Model):
    class Type(models.IntegerChoices):
        INCOME = 1, "Income"
        EXPENSE = 2, "Expense"

    class Reflection(models.IntegerChoices):
        HAPPY = 1, "Happy"
        NEUTRAL = 2, "Neutral"
        REGRET = 3, "Regret"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(choices=Type, default=Type.EXPENSE)
    category = models.ForeignKey(Category, related_name="records")
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    date = models.DateField()
    reflection = models.IntegerField(choices=Reflection, default=Reflection.NEUTRAL)


class Goal(models.Model):
    class Importance(models.IntegerChoices):
        MAJOR = 1, "Major"
        NORMAL = 2, "Normal"
        MINOR = 3, "MINOR"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField()
    deadline = models.DateField()
    importance = models.IntegerField(choices=Importance, default=Importance.NORMAL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")


class BudgetPeriod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_date = models.DateField()
    end_date = models.DateField()
    limit_amount = models.IntegerField()
    actual_spent = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgetPeriod"
    )
