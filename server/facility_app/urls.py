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
    path('facility/', FacilityAPI.as_view(), name='facility'),
    path('facility/<int:pk>/', FacilityAPI.as_view(), name='facility'),
    path('search_provider/', SearchProviderAPI.as_view(), name='search_provider'),
    path('search_provider/<int:pk>/', SearchProviderAPI.as_view(), name='search_provider'),
    path('wallet/', WalletAPI.as_view(), name='wallet'),
    path('wallet/<int:pk>/', WalletAPI.as_view(), name='wallet'),
    path('hiring-proposals/',HiringView.as_view(),name="hiring"),
    path('hiring-proposals/<int:pk>/',HiringView.as_view(),name="hiring"),
    path('accepts-applied-jobs/',AcceptsAppliedJobs.as_view(),name="accepts-applied-jobs"),
    path('accepts-applied-jobs/<int:pk>/',AcceptsAppliedJobs.as_view(),name="accepts-applied-jobs"),
    path('view_facility_rating/<int:pk>/',ViewFacilityRating.as_view(),name="view_facility_rating"),
    path('view_facility_rating/',ViewFacilityRating.as_view(),name="view_facility_rating"),
    path('give_rating_to_provider/',GiveRatingToProvider.as_view(),name="give_rating_to_provider"),
    path('cities/',Cities.as_view(),name="cities"),
    path('cities/<int:pk>/',Cities.as_view(),name="cities"),
]
