from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(JobPostModel)
class JobPostModelAdmin(ImportExportModelAdmin):
    list_display = ("zip_code", "city", "location", "job_status", "job_description", "to_datetime",  "from_datetime", "credentials", "hourly_rate", "user_id", "id")[::-1]

    date_hierarchy = "from_datetime"
    list_filter = ("from_datetime", "job_status", "city")
    search_fields = ("title",)


@admin.register(JobApplications)
class JobApplicationsModelAdmin(ImportExportModelAdmin):
    list_display = ("updated_at", "created_at", "status", "cover_letter", "job", "user", "id")[::-1]

    list_filter = ("status", )
    date_hierarchy = 'created_at'
