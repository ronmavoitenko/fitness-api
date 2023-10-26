from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user'),

urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

