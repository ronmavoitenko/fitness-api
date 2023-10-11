from django.db import models

# Create your models here.


class Exercises(models.Model):
    title = models.CharField(max_length=150)
    duration = models.TimeField()
    video = models.FileField(upload_to='media/exercises_video')
    break_time = models.TimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Workouts(models.Model):
    title = models.CharField(max_length=150)
    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/workout_image', null=True)
    duration = models.TimeField()
    calories = models.IntegerField()
    available = models.BooleanField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)