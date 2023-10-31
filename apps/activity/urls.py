from rest_framework.routers import DefaultRouter

from apps.activity.views import ActivityViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'', ActivityViewSet, basename='activity'),

urlpatterns = [] + router.urls

