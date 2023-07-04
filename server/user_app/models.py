from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from common_app.models import *
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils import timezone

# from rest_framework.authtoken.models import Token

# Create your models here.


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


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        values = [email, first_name, last_name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', "admin")
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, last_name, password, **extra_fields)




class ROLE_STATUS(models.TextChoices):
        admin = ('admin', 'admin')
        facility = ('facility', 'facility')
        provider = ('provider', 'provider')

class CustomUser(AbstractBaseUser, PermissionsMixin):

    SERVICE_STATUS = [
        ('Allergy and Asthma', 'Allergy and Asthma'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('MD', 'MD'),
        ('Medical Director', 'Medical Director'),
        ('BHT/ Medical Staff', 'BHT/ Medical Staff')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=ROLE_STATUS.choices)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # eligible_service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    # def get_short_name(self):
    #     return self.first_name
    
    class Meta:
        verbose_name = 'Manage User'
        verbose_name_plural = 'Manage Users'
    
class RegistrationLinkModel(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Manage Registration Link'
        verbose_name_plural = 'Manage Registration Links'


class ProfilePicModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media\images', default="images/default.png")
    banner_pic=models.ImageField(upload_to='media\images',null=True)

    def __str__(self):
        return str(self.user)



class BaseProfileModel(models.Model):
    CHOICES = (
        ('english', 'English'),
        ('gujarati', 'Gujarati'),
        ('hindi', 'Hindi'),
    )
    def get_default_date():
        return date.today()

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zipcode = models.PositiveIntegerField(validators=[validate_zipcode])
    phone_number = PhoneNumberField(verbose_name="phone number", validators=[validate_ten_digits])
    whatsapp_number = PhoneNumberField(blank=True, null=True)
    about_us=models.CharField(max_length=500,default='')
    language_info=models.CharField(max_length=20, choices=CHOICES,default='English')
    bank_account = models.PositiveBigIntegerField(null=True)
    instagram_info = models.URLField(max_length=200)    
    facebook_info = models.URLField(max_length=200)    
    bank_update_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.user)

class NotificationModel(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content=models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    is_read=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Manage Notification'
        verbose_name_plural = 'Manage Notification'

class RatingModel(models.Model):
    rated_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='given_ratings')
    rated_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='received_ratings')
    stars = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stars)

    class Meta:
        verbose_name = 'Manage Rating'
        verbose_name_plural = 'Manage Ratings'