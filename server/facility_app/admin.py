from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter

# Register your models here.

@admin.register(FacilityModel)
class FacilityModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "user_id", "facility_name", "user_name", "profile_pic", "city", "address", "zipcode", "phone_number", "documents_applicant",
                    "professional_information", "achievement_information", "bank_account", "instagram_info", "facebook_info", 'bank_update_count')

    list_filter = ("city", "zipcode")


@admin.register(FacilityWalletModel)
class FacilityWalletModelAdmin(ImportExportModelAdmin):
    list_display = ("withdrawal_from_wallet", "add_to_wallet",
                    "balance", "facility_id", "id")[::-1]


@admin.register(RatingModel)
class RatingModelAdmin(ImportExportModelAdmin):
    list_display = ("created_at", "feedback", "rating",
                    "provider_id", "facility_id", "id")[::-1]

    list_filter = ("rating", "created_at")


@admin.register(TotalRatingModel)
class TotalRatingModelAdmin(admin.ModelAdmin):
    list_display = ("average_rating", "total",
                    "total_people", "facility_id", "id")[::-1]

    list_filter = ("average_rating", "facility_id")


@admin.register(HiringModel)
class HiringModelAdmin(ImportExportModelAdmin):
    list_display = ("status", "interview_time", "hourly_rate",
                    "job_open_for", "facility_email", "provider_email", "id")[::-1]

    list_filter = ("interview_time", "status")
