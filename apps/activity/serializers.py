from rest_framework import serializers
from apps.activity.models import Activity, Plan, Steps, Foods


class ActivitySerializer(serializers.ModelSerializer):
    calories = serializers.IntegerField()
    steps = serializers.IntegerField()

    class Meta:
        model = Activity
        fields = (
            "id",
            "calories",
            "steps",
            "water",
            "sleep",
            "my_tasks",
            "finished_tasks",
            "user_plan",
        )


class CreateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "steps",
            "calories",
            "sleep",
            "water",
            "today_date",
            "user_plan",
            "my_tasks",
            "finished_tasks",
            "started_task",
            "start_task",
            "end_task",
        )


class UpdateActivitySerializer(serializers.ModelSerializer):
    class Mets:
        model = Activity
        fields = (
            "sleep",
            "water",
            "today_date",
            "finished_tasks",
        )


class CreatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "calories",
            "steps",
            "water",
            "sleep",
        )


class CreateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = (
            "title",
            "description",
            "grams",
            "fats",
            "carbs",
            "proteins",
            "calories",
        )


class MyFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = (
            "title",
            "description",
            "calories",
        )


class CreateStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = (
            "distance",
            "steps_count",
            "start_time",
            "end_time",
            "activity",
        )

