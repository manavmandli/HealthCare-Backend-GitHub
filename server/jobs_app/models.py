from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_app.models import CustomUser
from commons_app.models import JOB_STATUS_CHOICES, JOB_TIMING_CHOICES, JOB_APPLICATION_STATUS_CHOICES, CityModel
from django.core.exceptions import ValidationError

# Create your models here.
class JobPostModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hourly_rate = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    credentials = models.TextField()
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    job_timings = models.PositiveSmallIntegerField(choices=JOB_TIMING_CHOICES.choices)
    title = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255, help_text="Description for the job")
    job_status = models.PositiveSmallIntegerField(choices=JOB_STATUS_CHOICES.choices, default=JOB_STATUS_CHOICES.open, verbose_name='status of the job')
    location = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING)
    zip_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Manage Job Post'
        verbose_name_plural = 'Manage Job Posting'
        ordering = ["-posted_on"]

    def __str__(self):
        return f"{self.user} - {self.title}"

    def clean(self):
        if self.from_datetime > self.to_datetime:
            raise ValidationError("Please select appropiate date.")
  
# class JOB_STATUS_CHOICES =   
  
class JobApplications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Provider")
    job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=JOB_APPLICATION_STATUS_CHOICES.choices,validators=[MaxValueValidator(len(JOB_APPLICATION_STATUS_CHOICES.choices) - 1)], default=JOB_APPLICATION_STATUS_CHOICES.applied)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)

    class Meta:
        verbose_name = 'Manage Applied Job Post'
        verbose_name_plural = 'Manage Applied Jobs Posts'


    def __str__(self):
        return f"{self.user_id} application for {self.job.__str__()}"
  
