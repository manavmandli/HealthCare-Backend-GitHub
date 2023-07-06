from django.contrib import admin
from .models import NotificationModel

# Register your models here.

@admin.register(NotificationModel)
class NotificationModelAdmin(admin.ModelAdmin):
    # list_display = ("is_read", "timestamp", "content", "reciever", "generated_by")[::-1]
    list_display = ("is_read", "timestamp", "content", "reciever")[::-1]
