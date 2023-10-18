import random

from django.utils import timezone
from django.contrib.auth import logout

from apps.user.models import User
from apps.user.serializers import UserSerializer, CreateUserSerializer, ForgotChangePasswordSerializer, \
    CheckCodeSerializer, UpdateProfileSerializer, ForgotPasswordSerializer, ChangePasswordSerializer

from apps.common.helpers import send_notification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.common.permissions import IsUserOwner
from rest_framework import viewsets, status


class UserRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        if self.action == "forgot":
            return ForgotPasswordSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = serializer.save(username=self.request.data["email"])
        user.set_password(serializer.validated_data['password'])
        user.save()

    @action(methods=['post'], detail=False, serializer_class=ForgotPasswordSerializer, url_path="forgot-pass")
    def forgot(self, *args, **kwargs):
        secret_code = ''.join(random.choices('0123456789', k=4))
        while User.objects.filter(verification_code=secret_code).exists():
            secret_code = ''.join(random.choices('0123456789', k=4))
        email = self.request.data["email"]
        user = User.objects.get(email=email)
        user.verification_code = secret_code
        user.verification_code_expires = timezone.now() + timezone.timedelta(minutes=1)
        user.save()
        send_notification(user.email, "Your secret key for confirming account", f"{secret_code}")
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=CheckCodeSerializer, url_path="sms_verification")
    def sms_verification(self, request, *args, **kwargs):
        code = str(self.request.data["secret_code"])
        user = User.objects.get(verification_code=code)
        if timezone.now() < user.verification_code_expires:
            if user:
                return Response({"success": True}, status.HTTP_200_OK)
        else:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=ForgotChangePasswordSerializer, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        new_password = request.data.get("new_password")
        code = request.data.get("code")

        user = User.objects.get(verification_code=code)

        if user:
            user.set_password(new_password)
            user.save()
            user.verification_code = None
            return Response({"success": True, "message": "Password changed successfully."}, status.HTTP_200_OK)


class UserChangesViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOwner]

    def get_serializer_class(self):
        if self.action == "update_account":
            return UpdateProfileSerializer
        if self.action == "change_password":
            return ChangePasswordSerializer

        return super().get_serializer_class()

    @action(methods=['post'], detail=False, serializer_class=UpdateProfileSerializer, url_path="update-account")
    def update_account(self, request, *args, **kwargs):
        request.user.first_name = request.data["first_name"]
        request.user.last_name = request.data["last_name"]
        request.user.email = request.data["email"]
        request.user.phone = request.data["phone"]
        request.user.birthdate = request.data["birthdate"]
        request.user.save()
        return Response({"success": True}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=None, url_path="logout")
    def logout(self, request):
        logout(request)
        return Response("Successfully logged out", status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, serializer_class=ChangePasswordSerializer, url_path="change-password")
    def change_password(self, request):
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response("The password was changed", status.HTTP_200_OK)
