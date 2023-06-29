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

@admin.register(BaseProfileModel)
class BaseProfileModel(admin.ModelAdmin): 			
    list_display=("id", "user", "city", "address", "zipcode", "phone_number", "whatsapp_number", "about_us", "language_info", "bank_account", "instagram_info", "facebook_info", "bank_update_count")


@admin.register(ProfilePicModel)
class ProfilePicModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "profile_pic", "banner_pic")