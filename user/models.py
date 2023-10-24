from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.tasks.models import Tasks
from apps.activity.models import Activity


class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    phone = models.CharField(max_length=30)
    profile_image = models.FileField(upload_to='media/profile_image', null=True)
    verification_code = models.CharField(max_length=5, null=True)
    verification_code_expires = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    tasks = models.ManyToManyField(Tasks, related_name='tasks', blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
