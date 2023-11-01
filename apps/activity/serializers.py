from rest_framework import serializers
from apps.activity.models import Activity, Plan, Steps, Foods


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = (
            "id",
            "all_calories",
            "all_steps",
            "water",
            "sleep",
            "my_tasks",
            "finished_tasks",
        )


class CreateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "all_steps",
            "all_calories",
            "sleep",
            "water",
            "today_date",
            "my_tasks",
            "finished_tasks",
            "started_task",
            "start_task",
            "end_task",
        )


class UpdateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "sleep",
            "water",
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
            "id",
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
        )

