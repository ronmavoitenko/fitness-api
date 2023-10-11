from django.db import models

# Create your models here.


class Foods(models.Model):
    title = models.CharField(max_length=150)
    fats = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    modified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
