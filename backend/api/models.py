import json
import os
import uuid
from abc import ABC, abstractmethod
from json import JSONDecodeError
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import certifi
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from openai import OpenAI

from .utils import generate_family_invite_code

os.environ["SSL_CERT_FILE"] = certifi.where()


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


class ai_abstract(ABC):
    @abstractmethod
    def prompt(self, text: str) -> str:
        raise NotImplementedError


class groq_ai(ai_abstract):
    system_prompt = (
        "You are an AI assistant inside a family finance app. "
        "Give concise, practical, supportive financial advice based on the user's data."
    )

    def __init__(self):
        api_key = settings.GROQ_API_KEY
        url = settings.GROQ_API_URL

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = OpenAI(api_key=api_key, base_url=url)

    def prompt(self, text: str) -> str:
        # The library handles the JSON encoding for you
        response = self.client.chat.completions.create(
            model="groq/compound",  # Example supported Groq model
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.2,
        )

        # Access the text via the choices attribute
        return response.choices[0].message.content


class gemini_ai(ai_abstract):
    system_prompt = (
        "You are an AI assistant inside a family finance app. "
        "Give concise, practical, supportive financial advice based on the user's data."
    )

    def prompt(self, text: str) -> str:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        payload = json.dumps(
            {
                "systemInstruction": {
                    "parts": [{"text": self.system_prompt}],
                },
                "contents": [
                    {
                        "parts": [{"text": text}],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                },
            }
        ).encode("utf-8")

        url = (
            f"{settings.GEMINI_API_URL}/"
            f"{settings.GEMINI_MODEL}:generateContent?key={api_key}"
        )

        request = Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise ValueError(
                f"Gemini request failed with status {exc.code}: {detail}"
            ) from exc
        except URLError as exc:
            raise ValueError(f"Gemini connection failed: {exc.reason}") from exc
        except JSONDecodeError as exc:
            raise ValueError("Gemini returned invalid JSON.") from exc

        try:
            parts = body["candidates"][0]["content"]["parts"]
            return "".join(part.get("text", "") for part in parts).strip()
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise ValueError("Gemini response did not contain advice text.") from exc
