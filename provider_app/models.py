from django.db import models
from facility_app.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.fields import ArrayField
from common_app.models import *

# from .utils import *

# # Create your models here.

class TitleModel(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


    



#experince information
class ExperienceModel(models.Model):

    working_type = (
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    title = models.OneToOneField(TitleModel, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=255)
    location = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.user) 

 

    
class EducationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    school = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    grade = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)



# basic information 
class ProviderModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    open_to_work = models.BooleanField(default=True)
    title = models.ForeignKey(JobTitlesModel, on_delete=models.CASCADE)
    completed_training = models.ManyToManyField(TrainingsModel, blank=True)

    # resume = models.FileField(validators=[validate_file_size])

    def __str__(self):
        return str(self.user)

    def get_completed_training(self):
        return ", ".join([p.training_name for p in self.completed_training.all()])




class JobApplicationsModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Provider Email", blank=True, null=True)
    job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=100)
    status = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)

    class Meta:
        verbose_name = 'Manage Applied Job Post'
        verbose_name_plural = 'Manage Applied Jobs Posts'


    def __str__(self):
        return f"{self.user} apply to {self.job}"
  


class ProfilePicturesModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self):
        return f"{self.user}"