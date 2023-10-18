from rest_framework import serializers
from apps.workouts.models import Foods, Exercises, UserDailyPlan, Workouts, PlanAchievedResult, StepsForPlan


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = (
            "id",
            "title",
            "duration",
            "video",
            "break_time",
        )


class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = (
            "id",
            "title",
            "grams",
            "fats",
            "carbs",
            "proteins",
            "calories",
            "plan",
        )


class UserDailyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDailyPlan
        fields = (
            "id",
            "calories",
            "steps",
            "sleep",
            "water",
            "today_date",
            "workouts",
        )


class PlanAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAchievedResult
        fields = (
            "id",
            "sleep",
            "water",
        )


class AllPlanAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAchievedResult
        fields = (
            "id",
            "calories",
            "steps",
            "sleep",
            "water",
        )


class WorkoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workouts
        fields = (
            "id",
            "title",
            "description",
            "image",
            "duration",
            "calories",
            "available",
            "exercises",
        )


class StepsForPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepsForPlan
        fields = (
                "distance",
                "steps",
                "start_time",
                "end_time",
        )


class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workouts
        fields = (
            "title",
            "description",
            "image",
            "duration",
            "calories",
        )
