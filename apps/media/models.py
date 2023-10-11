from django.db import models

# Create your models here.


class Media(models.Model):
    media = models.FileField(upload_to='media/')
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
