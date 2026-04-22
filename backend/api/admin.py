from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import BudgetPeriod, Category, Family, Goal, Record, User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username", "role", "family"]

    fieldsets = UserAdmin.fieldsets + (
        ("Role & Family", {"fields": ("role", "family")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register([Record, Goal, Category, BudgetPeriod, Family])
