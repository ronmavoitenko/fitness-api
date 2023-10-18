from django.db import models


class UserDailyPlan(models.Model):
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    today_date = models.DateTimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    workouts = models.ManyToManyField('Workouts', related_name='workouts', blank=True)


class PlanAchievedResult(models.Model):
    calories = models.IntegerField()
    steps = models.IntegerField()
    sleep = models.TimeField()
    water = models.FloatField()
    plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StepsForPlan(models.Model):
    distance = models.FloatField()
    steps = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)


class Foods(models.Model):
    title = models.CharField(max_length=150)
    grams = models.IntegerField()
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(UserDailyPlan, on_delete=models.CASCADE, null=True)


class Workouts(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    image = models.FileField(upload_to='media/workout_image', null=True)
    duration = models.TimeField()
    calories = models.IntegerField()
    available = models.BooleanField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField('Exercises', related_name='exercises', blank=True)


class Exercises(models.Model):
    title = models.CharField(max_length=150)
    duration = models.TimeField()
    video = models.FileField(upload_to='media/exercises_video', null=True)
    break_time = models.TimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
