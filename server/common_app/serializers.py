from rest_framework import serializers
from .models import *

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModel
        fields = "__all__"

class UserLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguagesModel
        fields = "__all__"

class JobTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitlesModel
        fields = "__all__"

class TrainingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingsModel
        fields = "__all__"
