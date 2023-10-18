from django.contrib import admin
from apps.workouts.models import Workouts, Exercises, Foods, UserDailyPlan, PlanAchievedResult, StepsForPlan

# Register your models here.

admin.site.register(Workouts)
admin.site.register(Exercises)
admin.site.register(UserDailyPlan)
admin.site.register(Foods)
admin.site.register(PlanAchievedResult)
admin.site.register(StepsForPlan)
