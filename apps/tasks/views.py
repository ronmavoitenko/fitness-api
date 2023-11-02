from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser

from apps.tasks.serializers import TaskSerializer, GetTaskSerializer, CreateTaskSerializer
from apps.tasks.models import Task


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("id")
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        if self.action == "list":
            return GetTaskSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser, ]

        return super(TasksViewSet, self).get_permissions()
