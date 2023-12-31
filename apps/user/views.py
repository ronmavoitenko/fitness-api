from rest_framework.parsers import MultiPartParser
from django.contrib.auth import logout

import config.settings
from apps.user.models import User
from apps.user.serializers import UserSerializer, CreateUserSerializer, ForgotChangePasswordSerializer, \
     CheckCodeSerializer, UpdateProfileSerializer, ForgotPasswordSerializer, ChangePasswordSerializer,\
     FeedbackSerializer, NewVerificationCodeSerializer

from apps.common.helpers import generate_code
from apps.common.helpers import send_notification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    parser_classes = [MultiPartParser]
    serializer_class = CreateUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(username=self.request.data["email"])
        user.set_password(serializer.validated_data['password'])
        user.save()

    @action(methods=['post'], detail=False, serializer_class=ForgotPasswordSerializer, url_path="forgot-password", permission_classes=[AllowAny])
    def forgot_password(self, *args, **kwargs):
        secret_code = generate_code()
        email = self.request.data["email"]
        user = User.objects.get(email=email)
        user.verification_code = secret_code
        user.save()
        send_notification(user.email, "Your secret key for confirming account", f"{secret_code}")
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CheckCodeSerializer, url_path="verify-code", permission_classes=[AllowAny])
    def verify_code(self, request, *args, **kwargs):
        code = str(self.request.data["secret_code"])
        user = User.objects.filter(verification_code=code)
        if user:
            return Response({"success": True}, status.HTTP_200_OK)
        else:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=ForgotChangePasswordSerializer, url_path="change-password", permission_classes=[AllowAny])
    def verification_change_password(self, request, *args, **kwargs):
        new_password = request.data.get("new_password")
        code = request.data.get("code")
        user = User.objects.get(verification_code=code)
        if user:
            user.set_password(new_password)
            user.save()
            user.verification_code = None
            return Response({"success": True, "message": "Password changed successfully."}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=UpdateProfileSerializer, url_path="update-account")
    def account_update(self, request, *args, **kwargs):
        serializer = UpdateProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=None, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response("Successfully logged out", status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=ChangePasswordSerializer, url_path="old-password")
    def change_old_password(self, request):
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response("The password was changed", status.HTTP_200_OK)
        else:
            return Response({"message": "Incorrect old password"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=FeedbackSerializer, url_path="feedback")
    def feedback(self, request, *args, **kwargs):
        feedback = request.data["feedback"]
        send_notification(config.settings.EMAIL_HOST_USER, f"Feedback from {self.request.user.email}", feedback)
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=NewVerificationCodeSerializer,
            url_path="resend-code")
    def resend_code(self, request, *args, **kwargs):
        email = self.request.data["email"]
        password = self.request.data["password"]
        user = User.objects.get(email=email)
        if user.check_password(password):
            secret_code = generate_code()
            send_notification(user.email, "Your secret key for verification account", f"{secret_code}")
            user.verification_code = secret_code
            user.save()
            return Response({"success": True}, status.HTTP_200_OK)
        else:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)