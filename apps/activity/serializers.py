from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from apps.activity.models import Plan, ActivityWater, ActivityFood, ActivityStep, ActivitySleep


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "calories",
            "steps",
            "sleep",
            "water",
            "tasks",
            "started_task",
            "start_task",
            "end_task",
        )


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySleep
        fields = (
            "id",
            "sleep",
        )


class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityWater
        fields = (
            "id",
            "water",
        )


class CreateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityFood
        fields = (
            "id",
            "title",
            "description",
            "grams",
            "fats",
            "carbs",
            "proteins",
            "calories",
        )


class GetAllCaloriesSerializer(serializers.ModelSerializer):
    all_calories = serializers.SerializerMethodField()
    foods = CreateFoodSerializer(many=True, read_only=True, source="activityfood")

    class Meta:
        model = ActivityFood
        fields = (
            "all_calories",
            "foods",
        )

    def get_all_calories(self, obj):
        plan = self.context["request"].user.plan
        total_calories = ActivityFood.objects.filter(plan=plan, created_at__date=timezone.now().date()).values('plan')\
            .annotate(total_calories=Sum('calories'))
        return total_calories


class MyFoodSerializer(serializers.ModelSerializer):
    all_calories = serializers.SerializerMethodField()

    class Meta:
        model = ActivityFood
        fields = (
            "id",
            "title",
            "description",
            "calories",
            "all_calories"
        )


class CreateStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStep
        fields = (
            "id",
            "distance",
            "steps_count",
            "start_time",
            "end_time",
        )


class GetAllStepsSerializer(serializers.ModelSerializer):
    all_steps = serializers.SerializerMethodField()
    steps = CreateStepsSerializer(many=True, read_only=True, source="activitystep")

    class Meta:
        model = ActivityStep
        fields = (
            "all_steps",
            "steps",
        )

    def get_all_steps(self, obj):
        plan = self.context["request"].user.plan
        total_steps = ActivityStep.objects.filter(plan=plan, created_at__date=timezone.now().date()).values('plan') \
            .annotate(total_steps=Sum('steps_count'))
        return total_steps
