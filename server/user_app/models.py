from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from uuid import uuid4
from commons_app.models import CityModel, UserLanguages, JobTitles, Trainings, JOB_TIMING_CHOICES
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

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
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, first_name, last_name, password, **extra_fields)

class ServiceModel(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

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
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

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

class PasswordResetLinkModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reset_uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    url_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reset_uuid.hex

class BaseProfileModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    about = models.TextField()
    address = models.TextField()
    banner_image = models.ImageField(upload_to="banners", blank=True, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING)
    languages = models.ManyToManyField(UserLanguages)
    zip_code = models.CharField(max_length=9)
    contact_number = PhoneNumberField()
    facebook_username = models.CharField(max_length=50, blank=True, null=True)
    instagram_username = models.CharField(max_length=30, blank=True, null=True)
    whatsapp_number = PhoneNumberField(blank=True, null=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

class EducationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    grade = models.CharField(max_length=255)
    # description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.first_name} - {self.degree_type}"
    
    class Meta:
        verbose_name = 'education record'
        verbose_name_plural = 'education records'

class ExperienceModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    facility_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    work_type = models.PositiveSmallIntegerField(choices=JOB_TIMING_CHOICES.choices)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.user) 

class ProviderProfileModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    open_to_work = models.BooleanField(default=True)
    title = models.ForeignKey(JobTitles, on_delete=models.DO_NOTHING)
    completed_trainings = models.ManyToManyField(Trainings, blank=True)
    
    class Meta:
        verbose_name = 'provider profile'
        verbose_name_plural = 'provider profiles'
    
class ProfilePicturesModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(verbose_name='profile picture', upload_to="profile_pictures", blank=True)

class ReportModel(models.Model):

    class report_status(models.TextChoices):
        profile_report = ('Profile report', 'Profile report')
        payment_report = ('Payment report', 'Payment report')
        recruitment_report = ('Recruitment report', 'Recruitment report')
        job_post_report = ('Job post report', 'Job post report')

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True, null=True)
    report_type = models.CharField(max_length=255, choices=report_status.choices)
    description = models.TextField()

    class Meta:
        verbose_name = 'Manage Report'
        verbose_name_plural = 'Manage Reports'

    def __str__(self):
        return str(self.user_id)

