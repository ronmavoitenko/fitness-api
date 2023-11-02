from django.db import models
from apps.tasks.models import Task

# Create your models here.


class Plan(models.Model):
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    today_date = models.DateTimeField(auto_now=True)
    my_tasks = models.ManyToManyField(Task, related_name='my_tasks', blank=True)
    started_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    start_task = models.DateTimeField(null=True, blank=True, default=None)
    end_task = models.DateTimeField(null=True, blank=True, default=None)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Step(models.Model):
    distance = models.FloatField()
    steps_count = models.IntegerField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Food(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    grams = models.IntegerField()
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

