from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(TitleModel)
class TitleModelAdmin(admin.ModelAdmin): 			
    list_display=("id", "title")


@admin.register(ProviderModel)
class ProviderModelAdmin(admin.ModelAdmin): 			
    list_display=("id", "user", "title", "get_completed_training")


# admin.site.register(ProviderModel)

@admin.register(ExperienceModel)
class ExperienceModelAdmin(admin.ModelAdmin): 			
    list_display=("id", "user", "title", "facility_name", "location", "start_date", "end_date")


@admin.register(EducationModel)
class EducationModelAdmin(admin.ModelAdmin): 			
    list_display=("id", "user","school", "degree_type", "field_of_study", "start_date", "end_date", "grade")

@admin.register(JobApplicationsModel)
class JobApplicationsModelAdmin(ImportExportModelAdmin):
    list_display = ("updated_at", "created_at", "status", "cover_letter", "job", "user", "id")[::-1]

    list_filter = ("status", "job")
    date_hierarchy = 'created_at'


@admin.register(ProfilePicturesModel)
class ProfilePicturesModelAdmin(admin.ModelAdmin): 			
    list_display=("id", "user", "profile_picture")
