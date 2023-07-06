from django.db import models
from facility_app.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework import status
from user_app.models import CustomUser
# from .utils import *

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

class ProviderModel(models.Model):

    available_list = [
        ('available', 'available'),
        ('not available', 'not available')
    ]


    # Documents for Personal File

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    category = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="Backend/media/images/default.png", default="images/default.png")
    phone_number = models.PositiveBigIntegerField(verbose_name="phone number", blank=True, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.PositiveIntegerField(validators=[validate_zipcode])
    available = models.CharField(max_length=255, choices=available_list, default="available")
    hourly_rate = models.PositiveIntegerField()
    resume = models.FileField(validators=[validate_file_size])
    job_description = models.CharField(max_length=255)
    employment_verfication = models.FileField(validators=[validate_file_size])
    orignal_degree = models.FileField(validators=[validate_file_size])
    license_and_verfication = models.FileField(validators=[validate_file_size])
    dea_license = models.FileField(validators=[validate_file_size])
    cds_license = models.FileField(validators=[validate_file_size])
    npdb = models.FileField(validators=[validate_file_size], help_text="MD Only", blank=True, null=True) # MD Only
    peer_attestation_form = models.FileField(validators=[validate_file_size], help_text="Medical Director Only", blank=True, null=True) # Medical Director Only
    cpr_certification = models.FileField(validators=[validate_file_size], help_text="BHT/ Medical staff", blank=True, null=True) # BHT/ Medical staff
    bank_account = models.PositiveBigIntegerField()
    instagram_info = models.URLField(max_length=500, blank=True, null=True)    
    facebook_info = models.URLField(max_length=500, blank=True, null=True)    

    # Documents for Identification File

    I_9_Form = models.FileField(validators=[validate_file_size])
    id_proof = models.FileField(validators=[validate_file_size])
    w4_w9_1099 = models.FileField(validators=[validate_file_size], help_text="w4/ w9/ 1099")
    check_registry = models.FileField(validators=[validate_file_size])
    state_background_check = models.FileField(validators=[validate_file_size])

    # Trainings

    orientation = models.BooleanField(default=False)
    confidentiality = models.BooleanField(default=False)
    infection_prevention_and_control = models.BooleanField(help_text="Infection Prevention and Control", default=False)
    pain_management = models.BooleanField(default=False) # MEDICAL ONLY
    universal_precautions = models.BooleanField(default=False)
    patient_rights = models.BooleanField(default=False)
    child_elder_or_disabled_abuse = models.BooleanField(help_text="Child/ Elder/ or Disabled Abuse", default=False)
    emergency_plan_or_procedures = models.BooleanField(help_text="Emergency Plan and Procedures", default=False)
    co_occurring_disorders = models.BooleanField(help_text="Co-Occurring Disorders", default=False)
    conflict_of_interest = models.BooleanField(default=False)
    cultural_diversity = models.BooleanField(default=False)
    ethics = models.BooleanField(default=False)
    domestic_violence = models.BooleanField(default=False)
    sexual_assault_and_abuse = models.BooleanField(help_text="Sexual Assault and Abuse", default=False)
    tuberculosis = models.BooleanField(default=False)
    fire_safety_fire_extinguisher_training = models.BooleanField(help_text="Fire Safety/ Fire Extinguisher Training", default=False)

    # Documents for Medical File

    pre_hiring_health_assessment = models.FileField(validators=[validate_file_size], help_text="Pre-Hire Health Assessment")
    tb_screening = models.FileField(validators=[validate_file_size])
    immunization_record = models.FileField(validators=[validate_file_size]) # MMR VACCINES
    flu_vaccination = models.FileField(validators=[validate_file_size])
    drug_screen = models.FileField(validators=[validate_file_size])

    # Verified apply

    verified = models.BooleanField(default=False, blank=True, null=True)

    # Bank Update Count and Verified Count

    bank_update_count = models.PositiveIntegerField(default=0, blank=True)
    verified_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Manage Provider Profile'
        verbose_name_plural = 'Manage Providers Profiles'

    
    
    # def save(self, *args, **kwargs):
    #     count = 0 
    #     if self.verified_count>=2:
    #         ...
    #     else:
    #         if self.verified_count == 0 and self.verified:

    #             subject = "Verifed by Health Care admin"
    #             message = f"{self.first_name} you are verified by admin of health care project"

    #             send_mail(subject, 'verfied_provider', self.user_id,
    #                                 {"message":message})
    #             self.verified_count+=1

                    
    #     super(ProviderModel, self).save(*args, **kwargs)

    
    def __str__(self):
        return str(self.user_id)


class WalletModel(models.Model):
    provider_id = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name="ProviderEmail", verbose_name="Provider Email")
    balance = models.PositiveBigIntegerField(blank=True, null=True, verbose_name="Total Balance")
    withdrawal_from_wallet = models.PositiveBigIntegerField(blank=True,null=True)

    class Meta:
        verbose_name = 'Manage Wallet'
        verbose_name_plural = 'Manage Wallets'

class ProviderRatingModel(models.Model):
    provider_id=models.ForeignKey(ProviderModel,on_delete=models.CASCADE, blank=True, null=True)
    facility_id= models.ForeignKey(FacilityModel,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):


    #     rating_user = ProviderRatingModel.objects.filter(facility_id=self.facility_id,provider_id=self.provider_id).exists()

    #     if str(rating_user)=="True":
    #         return Response({"status":False, "message":"User can not give another rating and feedback to facility"}, status=status.HTTP_400_BAD_REQUEST)


    #     else:

    #         super(ProviderRatingModel, self).save(*args, **kwargs)
            
    #         ratings = ProviderRatingModel.objects.filter(provider_id=self.provider_id)

    #         total_rating = sum(rating.rating for rating in ratings)

    #         rating_count = ratings.count()

    #         provider_average_rating = total_rating/rating_count

    #         is_exist = ProviderTotalRatingModel.objects.filter(provider_id=self.provider_id).exists()

    #         add_data = ProviderTotalRatingModel.objects.filter(provider_id=self.provider_id).first()

    #         if is_exist:
    #             add_data.average_rating = 0
    #             # add_data.total = 0
    #             add_data.total_people = 0
    #             add_data.average_rating+=provider_average_rating
    #             add_data.total+=total_rating
    #             add_data.total_people+=rating_count
    #             add_data.save()
    #         else:
    #             ProviderTotalRatingModel.objects.create(provider_id=self.provider_id, average_rating=provider_average_rating, total_people=rating_count)

    class Meta:
        verbose_name = 'Manage Provider Rating'
        verbose_name_plural = 'Manage Provider Ratings'
            
    def __str__(self):
        return str(self.facility_id)

class ProviderAverageRatingModel(models.Model):
    provider_id = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, blank=True, null=True)
    total_people = models.PositiveIntegerField(blank=True, null=True)
    # total = models.PositiveBigIntegerField(blank=True, null=True, verbose_name="Total Vote")
    average_rating = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.provider_id)}, {self.average_rating}"
    
    class Meta:
        verbose_name = 'Manage Pro Rating Avg'
        verbose_name_plural = 'Manage Pro Ratings Avg'