from django.db import models
from apps.tasks.models import Task

# Create your models here.


class Plan(models.Model):
    plan_calories = models.IntegerField()
    plan_steps = models.IntegerField()
    plan_sleep = models.TimeField()
    plan_water = models.FloatField()
    my_tasks = models.ManyToManyField(Task, related_name='my_tasks', blank=True)
    started_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    start_task = models.DateTimeField(null=True, blank=True, default=None)
    end_task = models.DateTimeField(null=True, blank=True, default=None)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Sleep(models.Model):
    sleep = models.TimeField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Water(models.Model):
    water = models.FloatField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Step(models.Model):
    distance = models.FloatField()
    steps_count = models.IntegerField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
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
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
