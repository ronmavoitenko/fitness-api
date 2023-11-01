from django.db import models
from apps.tasks.models import Tasks

# Create your models here.


class Plan(models.Model):
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    all_steps = models.IntegerField(default=0)
    all_calories = models.IntegerField(default=0)
    sleep = models.TimeField(default="00:00")
    water = models.FloatField(default=0)
    today_date = models.DateTimeField(auto_now=True)
    my_tasks = models.ManyToManyField(Tasks, related_name='my_tasks', blank=True)
    finished_tasks = models.ManyToManyField(Tasks, related_name='finished_tasks', blank=True)
    started_task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True)
    start_task = models.DateTimeField(null=True, blank=True, default=None)
    end_task = models.DateTimeField(null=True, blank=True, default=None)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Steps(models.Model):
    distance = models.FloatField()
    steps_count = models.IntegerField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Foods(models.Model):
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

