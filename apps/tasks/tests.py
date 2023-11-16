from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from apps.tasks.serializers import CreateTaskSerializer, GetTaskSerializer, TaskSerializer
from apps.tasks.views import TasksViewSet
from apps.user.models import User


class TaskViewSetTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TasksViewSet.as_view({'post': 'create'})
        self.user = User.objects.create(first_name="Roman", last_name="Voitenco", email="test@example.com",
                                        phone="069551170",
                                        password="1111")
        self.client.force_authenticate(user=self.user)

    def test_get_serializer_class(self):
        view = TasksViewSet()
        view.action = 'create'
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, CreateTaskSerializer)
        view.action = 'list'
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, GetTaskSerializer)
        view.action = 'update'
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, TaskSerializer)

    def test_get_permissions(self):
        url = reverse("task-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"title": "New Task", "duration": "00:30:00", "calories": 150})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

