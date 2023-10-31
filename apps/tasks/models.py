from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    video = models.FileField(upload_to='media/tasks_video', null=True)
    duration = models.TimeField()
    break_time = models.TimeField()
    calories = models.IntegerField()
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


