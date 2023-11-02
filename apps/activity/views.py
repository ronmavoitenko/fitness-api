from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Tasks
from apps.activity.models import Activity, Plan, Steps, Foods
from apps.activity.serializers import ActivitySerializer, CreatePlanSerializer, CreateFoodSerializer, \
    CreateStepsSerializer, MyFoodSerializer, CreateActivitySerializer, UpdateActivitySerializer
from apps.tasks.serializers import TaskSerializer


class ActivityViewSet(viewsets.ModelViewSet):
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
        if self.action == "my_tasks":
            return TaskSerializer
        if self.action == "foods":
            return MyFoodSerializer
        if self.action == "update_activity":
            return UpdateActivitySerializer

        return ActivitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return Activity.objects.none()
        if self.action == "my_tasks":
            return self.request.user.activity.my_tasks.all().order_by("id")
        if self.action == "foods":
            return Foods.objects.filter(activity=self.request.user.activity).order_by("id")

        return queryset

    def perform_create(self, serializer):
        activity = serializer.save()
        self.request.user.activity = activity
        self.request.user.save()

    @action(methods=['post'], detail=False, serializer_class=UpdateActivitySerializer, url_path="update-activity")
    def update_activity(self, request, *args, **kwargs):
        activity = self.request.user.activity
        activity.sleep = request.data["sleep"]
        activity.water = request.data["water"]
        total_calories = Foods.objects.filter(activity=activity, created_at__date=timezone.now().date()).aggregate(total_calories=Sum('calories'))[
            'total_calories']
        total_steps = Steps.objects.filter(activity=activity, created_at__date=timezone.now().date()).aggregate(total_steps=Sum('steps_count'))['total_steps']
        activity.all_steps = total_steps
        activity.all_calories = total_calories
        activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=None, url_path="remove-daily-achievements")
    def remove_daily_achievements(self, request):
        activity = self.request.user.activity
        if timezone.now().strftime('%Y-%m-%d') > activity.today_date.strftime('%Y-%m-%d'):
            activity.sleep = "00:00"
            activity.water = 0
            activity.all_steps = 0
            activity.all_calories = 0
            activity.today_date = timezone.now()
            activity.finished_tasks.clear()
            activity.save()
            return Response("Daily achievements was removed", status.HTTP_200_OK)
        return Response("It's impossible to do that today ", status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CreatePlanSerializer, url_path="create-plan")
    def create_plan(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        request.user.plan = plan
        request.user.save()
        return Response({"success": True}, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=CreatePlanSerializer, url_path="change-plan")
    def change_plan(self, request, *args, **kwargs):
        plan = Plan.objects.get(id=request.user.plan.id)
        plan.steps = request.data["steps"]
        plan.calories = request.data["calories"]
        plan.sleep = request.data["sleep"]
        plan.water = request.data["water"]
        plan.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CreateFoodSerializer, url_path="create-food")
    def create_food(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity = Activity.objects.get(id=request.user.activity.id)
        serializer.save(activity=activity)
        return Response({"success": True}, status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, serializer_class=None, url_path="delete-food")
    def delete_food(self, *args, **kwargs):
        food_id = kwargs.get("pk")
        food = Foods.objects.get(id=food_id)
        food.delete()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="foods")
    def foods(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['post'], detail=False, serializer_class=CreateStepsSerializer, url_path="create-steps")
    def create_steps(self, request, *args, **kwargs):
        activity = self.request.user.activity
        distance = request.data["distance"]
        steps_count = request.data["steps_count"]
        start_time = request.data["start_time"]
        end_time = request.data["end_time"]
        Steps.objects.create(distance=distance, steps_count=steps_count, start_time=start_time, end_time=end_time, activity=activity)
        return Response({"success": True}, status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="my-tasks")
    def my_tasks(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="add-to-my-tasks")
    def add_to_my_tasks(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = Activity.objects.get(id=self.request.user.activity.id)
        activity.my_tasks.add(task)
        activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="delete-from-my-tasks")
    def delete_from_my_tasks(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = Activity.objects.get(id=self.request.user.activity.id)
        activity.my_tasks.remove(task)
        activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="start-task")
    def start_task(self, *args, **kwargs):
        task = Tasks.objects.get(id=kwargs.get("pk"))
        activity = self.request.user.activity
        task_exists = activity.my_tasks.filter(id=task.id).exists()
        if task_exists:
            activity.started_task = task
            activity.start_task = timezone.now()
            activity.save()
            return Response({"success": True}, status.HTTP_200_OK)
        return Response({"success": False}, status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="stop-task")
    def stop_task(self, *args, **kwargs):
        activity = self.request.user.activity
        activity.end_task = timezone.now()
        activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="continue-task")
    def continue_task(self, *args, **kwargs):
        activity = self.request.user.activity
        task = activity.started_task
        task_duration = timedelta(hours=task.duration.hour, minutes=task.duration.minute)
        time_elapsed = activity.end_task - activity.start_task
        if time_elapsed < task_duration:
            activity.end_task = None
            activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=None, url_path="cancel-task")
    def cancel_task(self, *args, **kwargs):
        activity = self.request.user.activity
        activity.start_task = None
        activity.end_task = None
        activity.started_task = None
        activity.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['get'], detail=False, serializer_class=None, url_path="finish-task")
    def finish_task(self, *args, **kwargs):
        activity = self.request.user.activity
        task = activity.started_task
        if task:
            if activity.end_task is None:
                activity.end_task = timezone.now()
            time_elapsed = activity.end_task - activity.start_task
            task_duration = timedelta(hours=task.duration.hour, minutes=task.duration.minute)

            if time_elapsed > task_duration:
                activity.start_task = None
                activity.started_task = None
                activity.finished_tasks.add(task)
                activity.save()
        return Response({"success": True}, status.HTTP_200_OK)
