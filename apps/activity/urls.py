from rest_framework.routers import DefaultRouter

from apps.activity.views import PlanViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'plan', PlanViewSet, basename='plan'),

urlpatterns = [] + router.urls

