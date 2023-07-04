"""Health_care_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view(), name="login"),
    path('login/<int:pk>/', UserLoginView.as_view(), name="login"),
    path('activate/<uuid:reset_uuid>/', ActivateView.as_view(), name="activate"),
    path('user_profile/<int:pk>/', UserProfileView.as_view(), name="user_profile"),
    path('user_profile/', UserProfileView.as_view(), name="user_profile"),
    path('user_rating',UserRatingView.as_view()),
    path('notification/<int:id>',NotificationView.as_view(),name="notification"),
    path('notification',NotificationView.as_view(),name="notification"),
]
