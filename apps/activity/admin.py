from django.contrib import admin
from apps.activity.models import Plan, Activity, Food, Step


admin.site.register(Food)
admin.site.register(Step)
admin.site.register(Activity)
admin.site.register(Plan)
