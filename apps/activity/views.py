from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Tasks
from apps.user.models import User
from apps.activity.models import Activity, Plan, Steps, Foods
from apps.activity.serializers import ActivitySerializer, CreatePlanSerializer, CreateFoodSerializer, \
    CreateStepsSerializer, MyFoodSerializer, CreateActivitySerializer
from apps.tasks.serializers import TaskSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateActivitySerializer
        if self.action == "create_plan":
            return CreatePlanSerializer
        if self.action == "create_food":
            return CreateFoodSerializer
        if self.action == "create_steps":
            return CreateStepsSerializer
        if self.action in ["my_tasks", "list"]:
            return TaskSerializer
        if self.action == "food":
            return MyFoodSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "my_tasks":
            return Tasks.objects.filter(activity__my_tasks=self.request.user)
        if self.action == "food":
            return Foods.objects.filter(activity__user_plan__user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        pass  # change only user_plan, all would be by default

    def perform_update(self):
        pass  # here update and if is next day, change steps, water and other by default, need write another serializer

    @action(methods=['post'], detail=False, serializer_class=CreatePlanSerializer, url_path="create-plan")
    def create_plan(self, request, *args, **kwargs):
        plan = request.data
        Plan.objects.create(plan)
        return Response(plan, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=CreatePlanSerializer, url_path="change-plan")
    def change_plan(self, request, *args, **kwargs):
        plan = Plan.objects.get(id=request.user.activity.user_plan)
        plan.steps = request.data["steps"]
        plan.calories = request.data["calories"]
        plan.sleep = request.data["sleep"]
        plan.water = request.data["water"]
        plan.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CreateFoodSerializer, url_path="create-food")
    def create_food(self, request, *args, **kwargs):
        food = request.data
        Foods.objects.create(food)
        return Response(food, status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, serializer_class=None, url_path="delete_food")
    def delete_food(self, *args, **kwargs):
        food_id = kwargs.get("pk")
        Foods.delete(food_id)
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="foods")
    def food(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['post'], detail=False, serializer_class=CreateStepsSerializer, url_path="create-steps")
    def create_steps(self, request, *args, **kwargs):
        steps = request.data
        Steps.objects.create(steps)
        return Response(steps, status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="my-tasks")
    def my_tasks(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="add-to-my")
    def add_to_my_tasks(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = Activity.objects.get(user_plan__user=self.request.user)
        activity.my_tasks.append(task)
        activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="delete-from-my")
    def delete_from_my_tasks(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = Activity.objects.get(user_plan__user=self.request.user)
        activity.my_tasks.remove(task)
        activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="start-task")
    def start_task(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = Activity.objects.get(user_plan__user=self.request.user)
        if len(activity.started_task) == 0:
            activity.started_task.append(task)
            activity.start_task = timezone.now()
            activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="stop-task")
    def stop_task(self, *args, **kwargs):
        activity = Activity.objects.get(user_plan__user=self.request.user)
        activity.end_task = timezone.now()
        activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="cancel-task")
    def cancel_task(self, *args, **kwargs):
        activity = Activity.objects.get(user_plan__user=self.request.user)
        activity.start_task = None
        activity.started_task = None
        activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="finish-task")
    def finish_task(self, *args, **kwargs):
        task = User.objects.filter(user=self.request.user, activity__started_task__isnull=False).first()
        activity = Activity.objects.get(user_plan__user=self.request.user)
        if task:
            if activity.end_task == None:
                activity.end_task = timezone.now()
            if activity.end_task - activity.start_task > task.duration:
                activity.start_task = None
                activity.started_task = None
                activity.finished_tasks.append(task)
                activity.save()
        return Response({"success": True}, status.status.HTTP_200_OK)

