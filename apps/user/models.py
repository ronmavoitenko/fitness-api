from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.workouts.models import Workouts

# Create your models here.


class User(AbstractUser):
    birthdate = models.DateTimeField(null=True)
    phone = models.CharField(max_length=30)
    profile_image = models.FileField(upload_to='media/profile_image', null=True)


class Foods(models.Model):
    title = models.CharField(max_length=150)
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


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

