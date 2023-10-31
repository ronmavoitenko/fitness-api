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
    steps = models.IntegerField(default=0)                                                              # 0
    calories = models.IntegerField(default=0)                                                           # 0
    sleep = models.TimeField(null=True)                                                                 # null
    water = models.FloatField(default=0)                                                                # 0
    today_date = models.DateTimeField(auto_now=True)                                                    # date now
    user_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)                            # plan_id
    my_tasks = models.ManyToManyField(Tasks, related_name='my_tasks', blank=True)                       # null
    finished_tasks = models.ManyToManyField(Tasks, related_name='finished_tasks', blank=True)           # null
    started_task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True)                        # null
    start_task = models.DateTimeField(null=True)                                                        # null
    end_task = models.DateTimeField(null=True)                                                          # null
    modified_at = models.DateTimeField(auto_now=True, null=True)                                        # null
    created_at = models.DateTimeField(auto_now_add=True)                                                # date now


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




# Add ForeignKey of activity to user, that can be null