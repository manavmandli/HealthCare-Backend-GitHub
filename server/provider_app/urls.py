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
    path('provider/', ProviderAPI.as_view(), name='provider'),
    path('provider/<int:pk>/', ProviderAPI.as_view(), name='provider'),
    path('search_facility/', SearchFacilityAPI.as_view(), name='search_facility'),
    path('search_facility/<int:pk>/', SearchFacilityAPI.as_view(), name='search_facility'),
    path('accept-hiring-proposals/',AcceptHiring.as_view(),name="hiring"),
    path('accept-hiring-proposals/<int:pk>/',AcceptHiring.as_view(),name="hiring"),
    path('view_provider_rating/<int:pk>/', ViewProviderRating.as_view(), name="view_provider_rating"),
    path('view_provider_rating/', ViewProviderRating.as_view(), name="view_provider_rating"),
    path('give_rating_to_facility/', GiveRatingToFacility.as_view(), name="give_rating_to_facility"),
    path('average_rating_provider/', AverageRatingProvider.as_view(), name='average_rating_provider'),
    path('average_rating_provider/<int:pk>/', AverageRatingProvider.as_view(), name='average_rating_provider'),
]
