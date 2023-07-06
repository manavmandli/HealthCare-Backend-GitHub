from django.urls import path
from .views import *

urlpatterns = [
    path('jobs/', JobPostAPI.as_view(), name='post-job'),
    path('jobs/<int:pk>/', JobPostAPI.as_view(), name='post-job'),
    path('job-applications/', JobApplicationsAPI.as_view(), name='job-applications'),
    path('job-applications/<int:pk>/', JobApplicationsAPI.as_view(), name='job-application'),
]