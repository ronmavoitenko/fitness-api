from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.workouts.models import UserDailyPlan
# Create your models here.


class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    phone = models.CharField(max_length=30)
    profile_image = models.FileField(upload_to='media/profile_image', null=True)
    verification_code = models.CharField(max_length=5, null=True)
    verification_code_expires = models.DateTimeField(null=True)
    user_daily_plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
