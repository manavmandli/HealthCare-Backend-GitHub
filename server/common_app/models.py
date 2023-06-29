from django.db import models

# Create your models here.

class CityModel(models.Model):
    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.city_name


class ServiceModel(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class JOB_STATUS_CHOICES(models.IntegerChoices):
    open = (0, 'Open')
    cancelled = (1, 'Cancelled')
    finished = (2, 'Finished')


class JOB_TIMING_CHOICES(models.IntegerChoices):
    part_time = (0, 'Part time')
    full_time = (1, 'Full time')


class UserLanguagesModel(models.Model):
    language = models.CharField(max_length=255)
    
    def __str__(self):
        return self.language
    
    class Meta:
        verbose_name = 'language'
        verbose_name_plural = 'languages'


class JobTitlesModel(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'work title'
        verbose_name_plural = 'work titles'


class TrainingsModel(models.Model):
    training_name = models.CharField(max_length=255)

    def __str__(self):
        return self.training_name

    class Meta:
        verbose_name = "Provider training"
        verbose_name_plural = "Providers trainings"