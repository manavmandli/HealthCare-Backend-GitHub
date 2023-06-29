from rest_framework import serializers
from .models import *
from provider_app.models import *
from provider_app.serializers import *

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityModel 
        fields = "__all__"



class FacilityJobPostingSerializer(serializers.ModelSerializer):

    applications = serializers.SerializerMethodField(read_only=True)

    def get_applications(self, obj):
        applications = JobApplicationsModel.objects.filter(job__id=obj.id)

        serializer = JobApplicationsSerializer(applications, many=True)
        return serializer.data 

    class Meta:
        model = JobPostModel
        fields = "__all__"


class ProviderJobPostingSerializer(serializers.ModelSerializer):

    application_count = serializers.SerializerMethodField(read_only=True)

    def get_application_count(self, obj):
        return JobApplicationsModel.objects.filter(job__id=obj.id).count()
         


    class Meta:
        model = JobPostModel
        fields = "__all__"