from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
        )


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
        )


class CheckCodeSerializer(serializers.ModelSerializer):
    secret_code = serializers.IntegerField(min_value=000000, max_value=999999)

    class Meta:
        model = User
        fields = (
            "secret_code",
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "birthdate",
        )


class NewVerificationCodeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )


class ForgotChangePasswordSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    new_password = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            "new_password",
            "code",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password",
        )


class FeedbackSerializer(serializers.ModelSerializer):
    feedback = serializers.CharField(max_length=1000)

    class Meta:
        model = User
        fields = (
            "feedback",
        )
