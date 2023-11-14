from datetime import timedelta
from django.shortcuts import get_object_or_404

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Task
from apps.tasks.serializers import GetTaskSerializer
from apps.activity.models import Plan, ActivityFood, ActivityStep
from apps.activity.serializers import PlanSerializer, SleepSerializer, WaterSerializer, CreateFoodSerializer,\
    CreateStepsSerializer, GetAllStepsSerializer, GetAllCaloriesSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['id']
    serializer_class = PlanSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return Plan.objects.none()
        if self.action == "tasks":
            return self.request.user.plan.tasks.all().order_by("id")

        return queryset

    def perform_create(self, serializer):
        plan = serializer.save()
        self.request.user.plan = plan
        self.request.user.save()

    @action(methods=['patch'], detail=False, serializer_class=PlanSerializer, url_path="change")
    def change(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan, id=request.user.plan.id)
        plan.steps = request.data["steps"]
        plan.calories = request.data["calories"]
        plan.sleep = request.data["sleep"]
        plan.water = request.data["water"]
        plan.save()
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=SleepSerializer, url_path="sleep")
    def sleep(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=self.request.user.plan)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=WaterSerializer, url_path="water")
    def water(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=self.request.user.plan)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=CreateFoodSerializer, url_path="food")
    def food(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=self.request.user.plan)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, serializer_class=None, url_path="delete-food")
    def delete_food(self, *args, **kwargs):
        food = get_object_or_404(ActivityFood, pk=kwargs.get("pk"))
        food.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, serializer_class=GetAllCaloriesSerializer, url_path="calories")
    def calories(self, request, *args, **kwargs):
        foods = ActivityFood.objects.filter(plan=self.request.user.plan, created_at__date=timezone.now()).order_by("-id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = {
            'all_calories': serializer.data['all_calories'],
            'foods': CreateFoodSerializer(foods, many=True).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CreateStepsSerializer, url_path="step")
    def step(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=self.request.user.plan)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, serializer_class=GetAllStepsSerializer, url_path="steps")
    def steps(self, request, *args, **kwargs):
        steps = ActivityStep.objects.filter(plan=self.request.user.plan, created_at__date=timezone.now()).order_by("-id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = {
            'all_steps': serializer.data['all_steps'],
            'steps': CreateStepsSerializer(steps, many=True).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=GetTaskSerializer, url_path="tasks")
    def tasks(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['post'], detail=True, serializer_class=None, url_path="add-task")
    def add_task(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        plan = self.request.user.plan
        plan.tasks.add(task)
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['delete'], detail=True, serializer_class=None, url_path="delete-task")
    def delete_task(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        plan = self.request.user.plan
        plan.tasks.remove(task)
        return Response(status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['put'], detail=True, serializer_class=None, url_path="start-task")
    def start_task(self, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        plan = self.request.user.plan
        if plan.tasks.filter(id=task.id).exists():
            plan.started_task = task
            plan.start_task = timezone.now()
            plan.save()
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['put'], detail=False, serializer_class=None, url_path="continue-task")
    def continue_task(self, *args, **kwargs):
        plan = self.request.user.plan
        task_duration = timedelta(hours=plan.started_task.duration.hour, minutes=plan.started_task.duration.minute)
        if plan.end_task - plan.start_task < task_duration:
            plan.end_task = None
            plan.save()
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['put'], detail=False, serializer_class=None, url_path="cancel-task")
    def cancel_task(self, *args, **kwargs):
        plan = self.request.user.plan
        plan.start_task = plan.end_task = plan.started_task = None
        plan.save()
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['put'], detail=False, serializer_class=None, url_path="stop-task")
    def stop_task(self, *args, **kwargs):
        plan = self.request.user.plan
        if plan.started_task:
            plan.end_task = timezone.now()
            task_duration = timedelta(hours=plan.started_task.duration.hour, minutes=plan.started_task.duration.minute)
            if plan.end_task - plan.start_task > task_duration:
                plan.start_task = plan.started_task = plan.end_task = None
                plan.tasks.remove(plan.started_task)
        plan.save()
        return Response(PlanSerializer(plan).data, status.HTTP_200_OK)
