from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(ProviderModel)
class ProviderModelAdmin(ImportExportModelAdmin):
    list_display = ("verified_count", "bank_update_count", "verified", "drug_screen", "flu_vaccination", "immunization_record", "tb_screening", "pre_hiring_health_assessment", "fire_safety_fire_extinguisher_training", "tuberculosis", "sexual_assault_and_abuse", "domestic_violence", "ethics", "cultural_diversity", "conflict_of_interest", "co_occurring_disorders", "emergency_plan_or_procedures", "child_elder_or_disabled_abuse", "patient_rights", "universal_precautions", "pain_management", "infection_prevention_and_control", "confidentiality", "orientation", "state_background_check", "check_registry", "w4_w9_1099", "id_proof", "I_9_Form", "facebook_info", "instagram_info", "bank_account", "cpr_certification", "peer_attestation_form", "npdb", "cds_license", "dea_license", "license_and_verfication", "orignal_degree", "employment_verfication", "job_description", "resume", "hourly_rate", "available", "zipcode", "address", "city", "phone_number", "profile_pic", "category", "user_name", "user_id", "id")[::-1]

    list_filter = ("verified", "city", "category")



@admin.register(WalletModel)
class WalletModelAdmin(ImportExportModelAdmin):
    list_display = ("withdrawal_from_wallet", "balance", "provider_id", "id")[::-1]



@admin.register(ProviderRatingModel)
class ProviderRatingModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "feedback", "rating", "facility_id", "provider_id", "id")[::-1]

    list_filter = ("rating", "created_at")


@admin.register(ProviderAverageRatingModel)
class ProviderAverageRatingModelAdmin(admin.ModelAdmin):
    list_display = ("average_rating", "total_people", "provider_id", "id")[::-1]

    list_filter = ("average_rating", "provider_id")
