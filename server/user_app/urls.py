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
    path('change_password/', ChangePassword.as_view()),
    path('reset-password/', ResetPasswordSendLinkView.as_view(),name="reset-password"),
    path('reset-password/<uuid:uu_id>/', ResetPasswordFormView.as_view(),name="reset-password"),
    path('report/', ReportAPI.as_view(), name="report"),
    path('report/<int:pk>/', ReportAPI.as_view(), name="report"),
    path('base-profile/', BaseProfileAPI.as_view(), name='current-base-profile'),
    path('base-profile/<int:pk>/', BaseProfileAPI.as_view(), name='requested-base-profile'),
    path('provider-profile/', ProviderProfileAPI.as_view(), name='current-provider-profile'),
    path('provider-profile/<int:pk>/', ProviderProfileAPI.as_view(), name='requested-provider-profile'),
    path('profile-picture/', ProfilePictureAPI.as_view(), name='profile-pictures'),
    path('profile-pictures/<int:pk>/', ProfilePictureAPI.as_view(), name='profile-picture'),
    path('education-details/', EducationAPI.as_view(), name='requested-user-education'),
    path('education-details/<int:pk>/', EducationAPI.as_view(), name='current-user-education'),
    path('work-experiences/', WorkExperienceAPI.as_view(), name='requested-user-work-experience'),
    path('work-experiences/<int:pk>/', WorkExperienceAPI.as_view(), name='current-user-work-experience'),
]
