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
    path('facility_profile/', FacilityProfileView.as_view(), name="facility_profile"),
    path('facility_profile/<int:pk>/', FacilityProfileView.as_view(), name="facility_profile"),
    path('job_post/', JobPostAPI.as_view(), name="job_post"),
    path('job_post/<int:pk>/', JobPostAPI.as_view(), name="job_post")
]
