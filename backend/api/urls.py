from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    CategoryViewSet,
    CustomTokenObtainPairView,
    GoalViewSet,
    LogoutView,
    RecordViewSet,
    RegisterView,
    advice_view,
    budget_view,
    family_create_view,
    family_detail_view,
    family_join_view,
    family_leave_view,
    family_regenerate_invite_view,
    family_remove_member_view,
    family_request_approve_view,
    family_request_reject_view,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("records", RecordViewSet, basename="record")
router.register("goals", GoalViewSet, basename="goal")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("advice/", advice_view, name="advice"),
    path("budget/", budget_view, name="budget"),
    path("family/", family_detail_view, name="family_detail"),
    path("family/create/", family_create_view, name="family_create"),
    path("family/join/", family_join_view, name="family_join"),
    path("family/leave/", family_leave_view, name="family_leave"),
    path(
        "family/regenerate-invite/",
        family_regenerate_invite_view,
        name="family_regenerate_invite",
    ),
    path(
        "family/remove-member/", family_remove_member_view, name="family_remove_member"
    ),
    path(
        "family/requests/<uuid:request_id>/approve/",
        family_request_approve_view,
        name="family_request_approve",
    ),
    path(
        "family/requests/<uuid:request_id>/reject/",
        family_request_reject_view,
        name="family_request_reject",
    ),
    path("", include(router.urls)),
]
