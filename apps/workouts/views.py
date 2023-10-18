from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Sum

from apps.workouts.serializers import UserDailyPlanSerializer, ExerciseSerializer, WorkoutsSerializer, FoodsSerializer,\
    GoalsSerializer, PlanAchievementsSerializer, StepsForPlanSerializer, AllPlanAchievementsSerializer
from apps.workouts.models import Exercises, UserDailyPlan, Workouts, Foods, PlanAchievedResult, StepsForPlan
from apps.common.permissions import IsUserOwner


class DailyPlanViewSet(viewsets.ModelViewSet):
    serializer_class = UserDailyPlanSerializer
    queryset = UserDailyPlan.objects.all().order_by("id")
    permission_classes = [IsUserOwner]

    def get_serializer_class(self):
        if self.action == "create":
            return UserDailyPlanSerializer
        if self.action == "plan_achieve":
            return PlanAchievementsSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "plan_achieve":
            return queryset.filter(id=self.request.user.user_daily_plan.id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        user_daily_plan = serializer.save()
        user.user_daily_plan = user_daily_plan
        user.save()

    @action(methods=['patch'], detail=True, serializer_class=None, url_path="start_goal")
    def start_goal(self, request, *args, **kwargs):
        workout = Workouts.objects.get(id=kwargs.get("pk"))
        self.request.user.user_daily_plan.workouts.add(workout)
        return Response("Workout added to user's goals", status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=PlanAchievementsSerializer, url_path="plan-achieve")
    def plan_achieve(self, request, *args, **kwargs):
        user_daily_plan = request.user.user_daily_plan
        calories_aggregated = Foods.objects.filter(plan=user_daily_plan).aggregate(total_calories=Sum('calories'))
        calories = calories_aggregated.get('total_calories', 0)
        steps_aggregated = StepsForPlan.objects.filter(plan=user_daily_plan).aggregate(total_steps=Sum('steps'))
        steps = steps_aggregated.get('total_steps', 0)
        data = {
            'calories': calories,
            'steps': steps,
            'sleep': request.data["sleep"],
            'water': request.data["water"],
            'plan': user_daily_plan
        }
        obj, created = PlanAchievedResult.objects.get_or_create(plan=user_daily_plan, defaults=data)

        if not created:
            for attr, value in data.items():
                setattr(obj, attr, value)
            obj.save()
        return Response({"success": True}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=StepsForPlanSerializer, url_path="add-steps-log")
    def add_steps_log(self, request, *args, **kwargs):
        user_daily_plan = request.user.user_daily_plan
        StepsForPlan.objects.create(
            distance=request.data["distance"],
            steps=request.data["steps"],
            start_time=request.data["start_time"],
            end_time=request.data["end_time"],
            plan=user_daily_plan
        )
        return Response({"success": True}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="get-plan-achieve")
    def get_achieved_plan(self, request, *args, **kwargs):
        user_daily_plan = request.user.user_daily_plan
        plan_results = PlanAchievedResult.objects.filter(plan=user_daily_plan)
        serializer = AllPlanAchievementsSerializer(plan_results, many=True)
        return Response(serializer.data)


class ExercisesViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercises.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return ExerciseSerializer

        return super().get_serializer_class()


class WorkoutsViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutsSerializer
    queryset = Workouts.objects.all().order_by("id")
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action == "create":
            return WorkoutsSerializer
        if self.action == "goals_in_progress":
            return GoalsSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "goals_in_progress":
            queryset = queryset.filter(workouts__user=self.request.user)

        return queryset

    @action(methods=['get'], detail=False, serializer_class=GoalsSerializer, url_path="goals-in-progress")
    def goals_in_progress(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FoodsViewSet(viewsets.ModelViewSet):
    serializer_class = FoodsSerializer
    queryset = Foods.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return FoodsSerializer

        return super().get_serializer_class()
