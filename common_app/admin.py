from django.contrib import admin
from .models import * 

# Register your models here.

@admin.register(CityModel)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ("id", "city_name")

@admin.register(ServiceModel)
class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

@admin.register(UserLanguagesModel)
class UserLanguagesModelAdmin(admin.ModelAdmin):
    list_display = ("id", "language")

@admin.register(JobTitlesModel)
class JobTitlesModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

@admin.register(TrainingsModel)
class TrainingsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "training_name")


