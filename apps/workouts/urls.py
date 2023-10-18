from rest_framework.routers import DefaultRouter

from apps.workouts.views import DailyPlanViewSet, ExercisesViewSet, WorkoutsViewSet, FoodsViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'daily_plan', DailyPlanViewSet, basename='daily-plan'),
router.register(r'exercises', ExercisesViewSet, basename='exercises'),
router.register(r'workouts', WorkoutsViewSet, basename='workouts'),
router.register(r'foods', FoodsViewSet, basename='foods'),

urlpatterns = [] + router.urls

