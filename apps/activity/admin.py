from django.contrib import admin
from apps.activity.models import Plan, Activity, Foods, Steps


admin.site.register(Foods)
admin.site.register(Steps)
admin.site.register(Activity)
admin.site.register(Plan)
