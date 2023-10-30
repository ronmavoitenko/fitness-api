from rest_framework import serializers
from apps.tasks.models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"


class GetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = (
            "title",
            "video",
            "duration",
            "calories",
        )


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = (
            "title",
            "description",
            "video",
            "duration",
            "break_time",
            "calories",
        )
