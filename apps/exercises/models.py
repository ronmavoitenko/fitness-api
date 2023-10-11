from django.db import models
from apps.media.models import Media

# Create your models here.


class Exercises(models.Model):
    title = models.CharField(max_length=150)
    duration = models.TimeField()
    video = models.ForeignKey(Media, on_delete=models.CASCADE)
    break_time = models.TimeField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)