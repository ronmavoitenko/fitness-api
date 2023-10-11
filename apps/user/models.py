from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.media.models import Media
from apps.foods.models import Foods
from apps.workouts.models import Workouts

# Create your models here.


class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    phone = models.CharField(max_length=30)
    profile_image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True)

# class User(models.Model):
#     name = models.CharField(max_length=25)
#     surname = models.CharField(max_length=30)
#     birthdate = models.DateTimeField(null=True)
#     email = models.EmailField()
#     phone = models.CharField(max_length=30)
#     password = models.CharField(max_length=100)
#     profile_image = models.ForeignKey(Media, on_delete=models.CASCADE)
#     modified_at = models.DateTimeField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)


class UserDailyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.FloatField()
    water = models.FloatField()
    workouts = models.ForeignKey(Workouts, on_delete=models.CASCADE)
    ate_food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    today_date = models.DateTimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
