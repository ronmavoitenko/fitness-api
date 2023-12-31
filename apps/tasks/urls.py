from rest_framework.routers import DefaultRouter

from apps.tasks.views import TasksViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'tasks', TasksViewSet, basename='task'),

urlpatterns = [] + router.urls

