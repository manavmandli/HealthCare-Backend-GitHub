from rest_framework import serializers
from .models import *

class JobPostSerializer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField(read_only=True)
    timings = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
        
    def get_posted_by(self, obj):
        return obj.user.__str__()
    
    def get_timings(self, obj):
        return obj.get_job_timings_display()
    
    def get_city_name(self, obj):
        return obj.city.name
    
    def get_applicant_count(self, obj):
        return JobApplications.objects.filter(job__id=obj.id).count()
    
    class Meta:
        model = JobPostModel
        fields = "__all__"
        abstract = True

class JobApplicationsSerializer(serializers.ModelSerializer):
    applicant_name = serializers.SerializerMethodField(read_only=True)
    status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_applicant_name(self, obj):
        return obj.user.__str__()

    def get_status_text(self, obj):
        return obj.get_status_display()
    
    class Meta:
        model = JobApplications
        fields = "__all__"
        abstract = True


class UserJobApplicationsSerializer(JobApplicationsSerializer):
    job_details = serializers.SerializerMethodField(read_only=True)
    
    
    def get_job_details(self, obj):
        return JobPostSerializer(obj.job).data
    
    class Meta:
        model = JobApplications
        fields = "__all__"


class ProviderJobPostSerializer(JobPostSerializer):
    class Meta:
        model = JobPostModel
        fields = "__all__"
        
class FacilityJobPostSerializer(JobPostSerializer):
    applications = serializers.SerializerMethodField(read_only=True)
    
    def get_applications(self, obj):
        applications = JobApplications.objects.filter(job__id=obj.id)
        serializer = JobApplicationsSerializer(applications, many=True)
        return serializer.data 
    
    class Meta:
        model = JobPostModel
        fields = "__all__"