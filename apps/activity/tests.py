import datetime
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from apps.activity.models import Plan, ActivityFood
from apps.tasks.models import Task
from apps.user.models import User
from apps.activity.views import PlanViewSet


class PlanViewSetTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(first_name="Roman", last_name="Voitenco", email="test@example.com",
                                        phone="069551170",
                                        password="1111")
        self.client.force_authenticate(user=self.user)
        self.plan = Plan.objects.create(calories=2000, steps=10000, sleep='08:00:00', water=2.0)
        self.task = Task.objects.create(title='Task 1', description='Description 1', duration=datetime.time(hour=0, minute=10, second=0), calories=100)
        self.food = ActivityFood.objects.create(title='Test Food', description='Test Description', grams=100, fats=10,
                                                carbs=20, proteins=15, calories=200, plan=None)
        self.plan.tasks.add(self.task)
        self.user.plan = self.plan
        self.plan.started_task = self.task
        self.user.save()
        self.plan.save()

    def test_get_queryset(self):
        response = self.client.get('/activities/plan/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')
        response = self.client.get('/activities/plan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], Plan.objects.all().last().id)
        view = PlanViewSet()
        view.swagger_fake_view = True
        view.request = self.client.post('/activities/plan')
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)

    def test_plan_create(self):
        url = reverse("plan-list")
        data = {
            "calories": 1,
            "steps": 1,
            "sleep": "11:00",
            "water": 1,
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change(self):
        url = reverse("plan-change")
        data = { "steps": 1, "calories": 2, "sleep": "11:00", "water": 1,}
        response = self.client.patch(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sleep(self):
        url = reverse("plan-sleep")
        data = {"sleep": "11:00", }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_water(self):
        url = reverse("plan-water")
        data = {"water": 3, }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_food(self):
        url = reverse("plan-food")
        data = {
            "title": "1",
            "description": "1",
            "grams": 1,
            "fats": 1,
            "carbs": 1,
            "proteins": 1,
            "calories": 1,
            "plan": self.plan.id,
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_food(self):
        url = reverse("plan-delete-food", kwargs={"pk": self.food.id})
        response = self.client.delete(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calories(self):
        url = reverse("plan-calories")
        response = self.client.get(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_step(self):
        url = reverse("plan-step")
        data = {
            "distance": 1,
            "steps_count": 1,
            "start_time": "11:00",
            "end_time": "12:00",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_steps(self):
        url = reverse("plan-steps")
        response = self.client.get(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_task(self):
        url = reverse("plan-add-task", kwargs={"pk": self.task.id})
        response = self.client.post(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        url = reverse("plan-delete-task", kwargs={"pk": self.task.id})
        response = self.client.delete(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_start_task(self):
        url = reverse("plan-start-task", kwargs={"pk": self.task.id})
        response = self.client.put(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_continue_task(self):
        url = reverse("plan-continue-task")
        self.user.plan.start_task = timezone.now()
        self.user.plan.end_task = timezone.now() + timedelta(days=1)
        response = self.client.put(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse("plan-continue-task")
        self.user.plan.start_task = timezone.now()
        self.user.plan.end_task = timezone.now() + timedelta(minutes=1)
        response = self.client.put(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_task(self):
        url = reverse("plan-cancel-task")
        response = self.client.put(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stop_task(self):
        url = reverse("plan-stop-task")
        self.user.plan.start_task = timezone.now() - timedelta(days=1)
        response = self.client.put(url, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
