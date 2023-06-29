from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter

# Register your models here.

@admin.register(FacilityModel)
class FacilityModel(admin.ModelAdmin): 			
    list_display=("id", "user", "facility_name", "documents_applicant", "professional_information", "achivements_info")


@admin.register(JobPostModel)
class JobPostModel(admin.ModelAdmin): 			
    list_display=("id", "user", "hourly_rate", "credentials", "from_datetime", "to_datetime", "job_timings", "title", "job_description", "job_status", "location", "posted_on", "city", "zip_code")
