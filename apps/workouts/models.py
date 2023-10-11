from django.db import models
from apps.media.models import Media
from apps.exercises.models import Exercises

# Create your models here.


class Workouts(models.Model):
    title = models.CharField(max_length=150)
    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    image = models.ForeignKey(Media, on_delete=models.CASCADE)
    duration = models.TimeField()
    calories = models.IntegerField()
    available = models.BooleanField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
