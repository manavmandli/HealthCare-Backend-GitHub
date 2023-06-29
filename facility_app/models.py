from django.db import models
from user_app.models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# # Create your models here.



def validate_file_size(value):
    # 10 MB (10 * 1024 * 1024 bytes)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size should not exceed 10 MB.")
	

def validate_ten_digits(value):
    if len(str(value)) != 11:
        raise ValidationError("Phone number should equal to 11 digits.")

def validate_zipcode(value):
    if len(str(value)) > 7:
        raise ValidationError("Value should lower then 7 digit")


class FacilityModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=255, unique=True)
    documents_applicant = models.FileField(upload_to="Backend/media", validators=[validate_file_size])
    professional_information = models.TextField()
    achivements_info=models.TextField(max_length=300,default='')
    
    
    class Meta:
        verbose_name = 'Manage Facility Profile'
        verbose_name_plural = 'Manage Facilities Profiles'

    def __str__(self):
        return str(self.facility_name)


class JobPostModel(models.Model):

    job_filter_status = [
        ('MD', 'MD'),
        ('MBBS', 'MBBS'),
        ('DCH', 'DCH'),
        ('General', 'General'),
        ('Cardiologist', 'Cardiologist'),
    ]

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

    def __str__(self):
        return f"{self.user} - {self.title}"

    def clean(self):
        if self.from_datetime > self.to_datetime:
            raise ValidationError("Please select appropiate date.")