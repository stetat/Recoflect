from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):

    def __str__(self):
        return self.username


class Record(models.Model):
    class Type(models.IntegerChoices):
        INCOME = 1, 'Income'
        EXPENSE = 2, 'Expense'

    class Reflection(models.IntegerChoices):
        HAPPY = 1, 'Happy'
        NEUTRAL = 2, 'Neutral'
        REGRET = 3, 'Regret'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.UUID4,
        editable=False
    )
    type = models.IntegerField(
        choices=Type,
        default=Type.EXPENSE
    )
    category = models.ForeignKey(Category, related_name='records')
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    date = models.DateField()
    reflection = models.IntegerField(
        choices=Reflection,
        default=Reflection.NEUTRAL
    )

class Category(models.Model):
