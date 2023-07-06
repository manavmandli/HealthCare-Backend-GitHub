from rest_framework import serializers
from .models import *
from django.conf import settings
from phonenumber_field.phonenumber import phonenumbers
from commons_app.serializers import TrainingsSerializer
# from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'confirm_password', 'role', 'first_name', 'last_name', 'eligible_service')
    

    def create(self, validated_data):
        print(f"validated_data: {validated_data}")
        user = CustomUser.objects.create_user(
            email=validated_data.get['email'],
            role=validated_data.get['role'],
            password=validated_data.get['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            # eligible_service=validated_data.get('eligible_service', ''),
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = "__all__"

class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    language_names = serializers.SerializerMethodField(read_only=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)
    contact_number_details = serializers.SerializerMethodField(read_only=True)
    whatsapp_number_details = serializers.SerializerMethodField(read_only=True)
    # trainings = serializers.SerializerMethodField(read_only=True)

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_role(self, obj):
        return obj.user.role
    
    def get_language_names(self, obj):
        return [lang.language for lang in obj.languages.all()]
    
    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        try:
            profile_picture = ProfilePicturesModel.objects.get(user=request.user).profile_picture
            return request.build_absolute_uri(profile_picture.url)
        except ProfilePicturesModel.DoesNotExist:
            return request.build_absolute_uri(settings.STATIC_URL+"img/default_user.png")

    def get_contact_number_details(self, obj):
        if obj.contact_number:
            phone_details = phonenumbers.parse(number=str(obj.contact_number))
            return {'country_code': phone_details.country_code, 'number_without_ext': phone_details.national_number}
        else:
            return None
        
    def get_whatsapp_number_details(self, obj):
        if obj.whatsapp_number:
            phone_details = phonenumbers.parse(number=str(obj.whatsapp_number))
            return {'country_code': phone_details.country_code, 'number_without_ext': phone_details.national_number}
        else:
            return None

    


    class Meta:
        model = BaseProfileModel
        fields = "__all__"
        
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicturesModel
        fields = "__all__"
        
class ProviderProfileSerializer(serializers.ModelSerializer):
    title_name = serializers.SerializerMethodField(read_only=True)
    all_completed_trainings = serializers.SerializerMethodField(read_only=True)
    
    def get_title_name(self, obj):
        return obj.title.title 
    
    def get_all_completed_trainings(self, obj):
        try:
            return obj.completed_trainings.values('id', 'training_name')
        except ProviderProfileModel.DoesNotExist:
            return []
    
    class Meta:
        model = ProviderProfileModel
        fields = "__all__"
   
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = "__all__"
        
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceModel
        fields = "__all__"
