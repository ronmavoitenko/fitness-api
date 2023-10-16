from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserRegistrationViewSet, UserChangesViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserRegistrationViewSet, basename='user'),
router.register(r'user-changes', UserChangesViewSet, basename='changes'),

urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

