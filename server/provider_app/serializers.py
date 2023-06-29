from rest_framework import serializers
from .models import *

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderModel
        fields = "__all__"
        

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceModel
        fields = "__all__"

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = "__all__"

class JobApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationsModel
        fields = "__all__"

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicturesModel
        fields = "__all__"