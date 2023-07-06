from django.db import models
from user_app.models import CustomUser

# Create your models here.
class JOB_STATUS_CHOICES(models.IntegerChoices):
    open = (0, 'Open')
    cancelled = (1, 'Cancelled')
    completed = (2, 'Completed')
    
class JOB_APPLICATION_STATUS_CHOICES(models.IntegerChoices):
    waiting = (0, 'Waiting for response')
    applied = (1, 'Applied')
    accepted = (2, 'Accepted')
    rejected = (3, 'Rejected')
    
    
class JOB_TIMING_CHOICES(models.IntegerChoices):
    part_time = (0, 'Part time')
    full_time = (1, 'Full time')

class UserLanguages(models.Model):
    language = models.CharField(max_length=255)
    
    def __str__(self):
        return self.language
    
    class Meta:
        verbose_name = 'language'
        verbose_name_plural = 'languages'

class CityModel(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        
class JobTitles(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'work title'
        verbose_name_plural = 'work titles'
        
class Trainings(models.Model):
    training_name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'training'
        verbose_name_plural = 'trainings'

class Notifications(models.Model):
    reciever = models.ManyToManyField(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'