from django.db import models
from apps.tasks.models import Task
from apps.common.models import BaseModel

# Create your models here.


class Plan(BaseModel):
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    tasks = models.ManyToManyField(Task, related_name='my_tasks', blank=True)
    started_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    start_task = models.DateTimeField(null=True, blank=True, default=None)
    end_task = models.DateTimeField(null=True, blank=True, default=None)


class ActivitySleep(BaseModel):
    sleep = models.TimeField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)


class ActivityWater(BaseModel):
    water = models.FloatField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)


class ActivityStep(BaseModel):
    distance = models.FloatField()
    steps_count = models.IntegerField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)


class ActivityFood(BaseModel):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    grams = models.IntegerField()
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

