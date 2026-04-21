from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import CategoryViewSet, CustomTokenObtainPairView, GoalViewSet, RecordViewSet, RegisterView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("records", RecordViewSet, basename="record")
router.register("goals", GoalViewSet, basename="goal")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
