from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import UserLanguages, CityModel, JobTitles, Trainings

class UserLanguagesSerializer(ModelSerializer):
    class Meta:
        model = UserLanguages
        fields = "__all__"

class CitySerializer(ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"
        
        
class JobTitlesSerializer(ModelSerializer):
    class Meta:
        model = JobTitles
        fields = "__all__"
        
class TrainingsSerializer(ModelSerializer):
    class Meta:
        model = Trainings
        fields = "__all__"

