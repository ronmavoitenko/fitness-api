from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.permissions import AllowAny

from apps.user.models import User
from apps.user.views import UserViewSet


class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({'post': 'create'})
        self.user = User.objects.create(first_name="Roman", last_name="Voitenco", email="test@example.com",
                                        phone="069551170",
                                        password="1111")

    def test_get_permission(self):
        view = UserViewSet()
        view.action = 'create'
        permissions = view.get_permissions()
        self.assertTrue(isinstance(permissions[0], AllowAny))

    def test_create_user(self):
        url = reverse("user-list")
        data = {
            "first_name": "Roman",
            "last_name": "Voitenco",
            "email": "johndoe@example.com",
            "phone": "069551170",
            "password": "password",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_forgot_password(self):
        url = reverse("user-forgot-password")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_code(self):
        self.user.verification_code = 1111
        self.user.save()
        code = self.user.verification_code
        url = reverse("user-verify-code")
        data = {"secret_code": code}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {"secret_code": "1234"}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verification_change_password(self):
        self.user.verification_code = 1111
        self.user.save()
        new_password = "newpassword123"
        url = reverse("user-verification-change-password")
        data = {"code": 1111, "new_password": new_password}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_update(self):
        url = reverse("user-account-update")
        data = {"first_name": "NewName", "last_name": "NewLastName"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {"first_name": "NewName", "last_name": "NewLastName", "email": "1234"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        self.assertTrue(self.user.is_authenticated)
        url = reverse("user-logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_old_password_success(self):
        self.user.set_password("1111")
        url = reverse("user-change-old-password")
        self.client.force_authenticate(user=self.user)
        data = {
            "old_password": "1111",
            "new_password": "newpassword"
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_old_password_failure(self):
        url = reverse("user-change-old-password")
        self.client.force_authenticate(user=self.user)
        data = {
            "old_password": "wrong_password",
            "new_password": "2222"
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_feedback(self):
        url = reverse("user-feedback")
        data = {
            "feedback": "This is a test feedback"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_code(self):
        self.user.set_password("1111")
        self.user.save()
        url = reverse("user-resend-code")
        data = {
            "email": "test@example.com",
            "password": "1111"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_code_failure(self):
        url = reverse("user-resend-code")
        data = {
            "email": "test@example.com",
            "password": "wrong_password"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
