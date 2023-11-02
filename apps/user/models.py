from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.activity.models import Activity, Plan


class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    phone = models.CharField(max_length=30)
    profile_image = models.FileField(upload_to='media/profile_image', null=True)
    verification_code = models.CharField(max_length=5, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
