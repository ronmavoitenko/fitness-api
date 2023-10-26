from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.tasks.serializers import TaskSerializer, GetTaskSerializer, CreateTaskSerializer
from apps.tasks.models import Tasks


class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        if self.action == "list":
            return GetTaskSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser, ]
        else:
            self.permission_classes = [AllowAny, ]

        return super(TasksViewSet, self).get_permissions()

    def perform_create(self, serializer):
        task = serializer.save()
        task.save()
