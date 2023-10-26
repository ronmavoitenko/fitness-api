from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.tasks.views import TasksViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'tasks', TasksViewSet, basename='task'),

urlpatterns = [] + router.urls

