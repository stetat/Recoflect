import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone

from .utils import generate_family_invite_code


class UserQuerySet(models.QuerySet):
    def parents(self):
        return self.filter(role=1)

    def children(self):
        return self.filter(role=2)


class CustomUserManager(UserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = CustomUserManager()

    class Role(models.IntegerChoices):
        PARENT = 1, "Parent"
        CHILD = 2, "Child"
        NONE = 3, "None"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
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


class FamilyJoinRequest(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        APPROVED = 2, "Approved"
        REJECTED = 3, "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="join_requests"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="family_join_requests"
    )
    desired_role = models.IntegerField(choices=User.Role.choices)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=60)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories", null=True, blank=True
    )

    class Meta:
        unique_together = ("title", "user")


class RecordQuerySet(models.QuerySet):
    def income(self):
        return self.filter(type=1)

    def expenses(self):
        return self.filter(type=2)

    def happy(self):
        return self.filter(reflection=1)

    def neutral(self):
        return self.filter(reflection=2)

    def regret(self):
        return self.filter(reflection=3)


class RecordManager(models.Manager.from_queryset(RecordQuerySet)):
    pass


class Record(models.Model):
    objects = RecordManager()

    class Type(models.IntegerChoices):
        INCOME = 1, "Income"
        EXPENSE = 2, "Expense"

    class Reflection(models.IntegerChoices):
        HAPPY = 1, "Happy"
        NEUTRAL = 2, "Neutral"
        REGRET = 3, "Regret"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="records",
        null=True,
        blank=True,
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(choices=Type, default=Type.EXPENSE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="records"
    )
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    date = models.DateField()
    reflection = models.IntegerField(choices=Reflection, default=Reflection.NEUTRAL)


class GoalQuerySet(models.QuerySet):
    def major(self):
        return self.filter(importance=1)

    def normal(self):
        return self.filter(importance=2)

    def minor(self):
        return self.filter(importance=3)

    def overdue(self):
        return self.filter(deadline__lt=timezone.now().date())


class Goal(models.Model):
    class Importance(models.IntegerChoices):
        MAJOR = 1, "Major"
        NORMAL = 2, "Normal"
        MINOR = 3, "MINOR"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField()
    current_amount = models.IntegerField(default=0)
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
