from django.db import models
from user_app.models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from commons_app.models import JOB_STATUS_CHOICES, JOB_TIMING_CHOICES, CityModel

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
    if len(str(value)) > 9:
        raise ValidationError("Value should lower then 9 digit")


class FacilityModel(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True) 
    facility_name = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="Backend/media/images", default="images/default.png")
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zipcode = models.PositiveIntegerField(validators=[validate_zipcode])
    phone_number = models.PositiveIntegerField(verbose_name="phone number", validators=[validate_ten_digits])
    documents_applicant = models.FileField(upload_to="Backend/media", validators=[validate_file_size])
    professional_information = models.TextField()
    achievement_information = models.TextField()
    bank_account = models.PositiveBigIntegerField()
    instagram_info = models.URLField(max_length=500)    
    facebook_info = models.URLField(max_length=500)    
    bank_update_count = models.PositiveIntegerField(default=0, blank=True)
    
    class Meta:
        verbose_name = 'Manage Facility Profile'
        verbose_name_plural = 'Manage Facilities Profiles'

    def __str__(self):
        return str(self.facility_name)
    

class FacilityWalletModel(models.Model):
    facility_id = models.ForeignKey(FacilityModel, on_delete=models.CASCADE, related_name="facility_id", verbose_name="Facility Email")
    balance = models.PositiveBigIntegerField(blank=True, null=True, verbose_name="Total Balance")
    add_to_wallet = models.PositiveBigIntegerField(blank=True,null=True)
    withdrawal_from_wallet = models.PositiveBigIntegerField(blank=True,null=True)

    class Meta:
        verbose_name = 'Manage Wallet'
        verbose_name_plural = 'Manage Wallets'


# class TranscationModel(models.Model):
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     provider_id = models.ForeignKey('provider_app.ProviderModel', on_delete=models.CASCADE)
#     amount = models.PositiveBigIntegerField()

class RatingModel(models.Model):
    facility_id= models.ForeignKey(FacilityModel,on_delete=models.CASCADE,related_name='ratings_received')
    provider_id=models.ForeignKey('provider_app.ProviderModel',on_delete=models.CASCADE,related_name='ratings_given')
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        rating_user = RatingModel.objects.filter(facility_id=self.facility_id,provider_id=self.provider_id).exists()

        if str(rating_user)=="True":
            print("User can not give another rating and feedback to facility")


        else:

            super(RatingModel, self).save(*args, **kwargs)
            
            ratings = RatingModel.objects.filter(facility_id=self.facility_id)

            total_rating = sum(rating.rating for rating in ratings)

            rating_count = ratings.count()

            facility_average_rating = total_rating/rating_count

            is_exist = TotalRatingModel.objects.filter(facility_id=self.facility_id).exists()

            add_data = TotalRatingModel.objects.filter(facility_id=self.facility_id).first()

            if is_exist:
                add_data.average_rating = 0
                add_data.total = 0
                add_data.total_people = 0
                add_data.average_rating+=facility_average_rating
                add_data.total+=total_rating
                add_data.total_people+=rating_count
                add_data.save()
            else:
                TotalRatingModel.objects.create(facility_id=self.facility_id, total=total_rating, average_rating=facility_average_rating, total_people=rating_count)

    class Meta:
        verbose_name = 'Manage Facility Rating'
        verbose_name_plural = 'Manage Facilites Ratings'
            
    def __str__(self):
        return str(self.facility_id)
    

class TotalRatingModel(models.Model):
    facility_id = models.ForeignKey(FacilityModel, on_delete=models.CASCADE, blank=True, null=True)
    total_people = models.PositiveBigIntegerField(blank=True, null=True)
    total = models.PositiveBigIntegerField(blank=True, null=True, verbose_name="Total Vote")
    average_rating = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.facility_id)}, {self.average_rating}"
    
    class Meta:
        verbose_name = 'Manage Facility Rating Avg'
        verbose_name_plural = 'Manage Facilites Ratings Avg'
    

class HiringModel(models.Model):

    job_status = [
        ('Allergy and Asthma', 'Allergy and Asthma'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Endocrinology', 'Endocrinology'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General surgery', 'General surgery'),
        ('MD', 'MD'),
        ('Medical Director Only', 'Medical Director Only'),
        ('BHT/ Medical Staff', 'BHT/ Medical Staff')
    ]

    provider_email=models.ForeignKey("provider_app.ProviderModel", on_delete=models.CASCADE)
    facility_email=models.ForeignKey("facility_app.FacilityModel", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Facility")
    job_open_for = models.CharField(max_length=255, choices=job_status)
    hourly_rate = models.PositiveIntegerField()
    interview_time=models.DateTimeField()
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Manage Hiring Request'
        verbose_name_plural = 'Manage Hiring Requests'