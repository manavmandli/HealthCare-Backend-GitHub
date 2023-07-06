from django.urls import path, include
from .views import *

urlpatterns = [
    path("languages/", UserLanguagesAPI.as_view(), name="user-languages"),
    path("cities/", CitiesAPI.as_view(), name="cities"),
    path("job-titles/", JobTitlesAPI.as_view(), name="job-titles"),
    path("trainings/", TrainingsAPI.as_view(), name="trainings"),
]