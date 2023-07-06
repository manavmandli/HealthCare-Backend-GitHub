from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter


# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'role', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'role', 'first_name', 'last_name')
    ordering = ('email',)

    readonly_fields = ["date_joined"]

    def get_list_filter(self, request):
        """
        Override get_list_filter to add DateFieldListFilter for date_joined.
        """
        list_filter = super().get_list_filter(request)
        list_filter += (('date_joined', DateFieldListFilter),)
        return list_filter


@admin.register(CustomUser)
class CustomUserAdmin(CustomUserAdmin):
    pass


@admin.register(RegistrationLinkModel)
class RegistrationLinkModelAdmin(ImportExportModelAdmin):
    list_display = ("updated_at", "created_at", "reset_uuid", "user_id", "id")[::-1]

@admin.register(PasswordResetLinkModel)
class PasswordResetLinkModelAdmin(ImportExportModelAdmin):
    list_display = ("updated_at", "created_at", "url_link", "reset_uuid", "user", "id")[::-1]


@admin.register(ReportModel)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "role", "report_type", "description")


@admin.register(ServiceModel)
class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

@admin.register(BaseProfileModel)
class BaseProfileModelAdmin(admin.ModelAdmin):
    list_display = ("whatsapp_number", "instagram_username", "facebook_username", "contact_number", "zip_code", "city", "address", "about", "user")[::-1]

@admin.register(ProfilePicturesModel)
class ProfilePicturesModelAdmin(admin.ModelAdmin):
    list_display = ("profile_picture", "user")

@admin.register(ProviderProfileModel)
class ProviderProfileModelAdmin(admin.ModelAdmin):
    list_display = ("title", "open_to_work", "user")
    filter_horizontal = ("completed_trainings", )
    
@admin.register(EducationModel)
class EducationModelAdmin(admin.ModelAdmin):
    list_display = ("grade", "end_date", "start_date", "field_of_study", "degree_type", "school", "user")

@admin.register(ExperienceModel)
class ExperienceModelAdmin(admin.ModelAdmin):
    list_display = ("end_date", "start_date", "work_type", "location", "facility_name", "title", "user")[::-1]
