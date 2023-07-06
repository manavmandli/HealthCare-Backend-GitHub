from rest_framework import serializers
from .models import *
# from facility_app.serializers import JobPostSerializer

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderModel
        fields = "__all__"
        
class ProviderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRatingModel
        fields = "__all__"

class ProviderTotalRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAverageRatingModel
        fields = "__all__"