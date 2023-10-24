from django.db import models


class Activity(models.Model):
    calories = models.IntegerField()
    steps_count = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    today_date = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Steps(models.Model):
    distance = models.FloatField()
    steps_count = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Foods(models.Model):
    title = models.CharField(max_length=150)
    grams = models.IntegerField()
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
