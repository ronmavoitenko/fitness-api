from django.db import models

from apps.user.models import User


class UserDailyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.FloatField()
    water = models.FloatField()
    today_date = models.DateTimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Exercises(models.Model):
    title = models.CharField(max_length=150)
    duration = models.TimeField()
    video = models.FileField(upload_to='media/exercises_video')
    break_time = models.TimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Workouts(models.Model):
    plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/workout_image', null=True)
    duration = models.TimeField()
    calories = models.IntegerField()
    available = models.BooleanField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Foods(models.Model):
    title = models.CharField(max_length=150)
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_daily_plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)
