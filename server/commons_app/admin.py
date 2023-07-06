from django.contrib import admin
from .models import CityModel, UserLanguages, JobTitles, Trainings

# Register your models here.
@admin.register(CityModel)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    
@admin.register(UserLanguages)
class UserLanguagesAdmin(admin.ModelAdmin):
    list_display = ("language", "id")
    
@admin.register(JobTitles)
class JobTitlesAdmin(admin.ModelAdmin):
    list_display = ("title", "id")

@admin.register(Trainings)
class TrainingsAdmin(admin.ModelAdmin):
    list_display = ("training_name", )
