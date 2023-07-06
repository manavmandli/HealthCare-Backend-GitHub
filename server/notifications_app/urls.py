from django.urls import path
from .views import NotificationsAPI, NotificationBeatAPI

urlpatterns = [ 
    path(route="notifications/", view=NotificationsAPI.as_view(), name="user-notifications"),
    path(route="notification-beat/", view=NotificationBeatAPI.as_view(), name="notification-beat"),
]