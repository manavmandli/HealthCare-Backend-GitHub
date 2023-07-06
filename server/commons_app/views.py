from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from constants.status import codes
from .models import *
from .serializers import *

# Create your views here.

class JobTitlesAPI(APIView):
    def get(self, request):
        titles = JobTitles.objects.all()
        titles_serializer = JobTitlesSerializer(titles, many=True)
        return Response({"status": True, "titles": titles_serializer.data}, status=codes.OK)

class UserLanguagesAPI(APIView):
    def get(self, request):
        languages = UserLanguages.objects.all()
        languages_serializer = UserLanguagesSerializer(languages, many=True)
        return Response({"status": True, "languages": languages_serializer.data}, status=codes.OK)
            
class CitiesAPI(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                city = CityModel.objects.get(id=pk)
                cities_serializer = CitySerializer(city)    
            except CityModel.DoesNotExist:
                return Response({"status": False, "message": "Requested city is not added!"}, status=codes.CLIENT_ERROR)
        else:
            cities = CityModel.objects.all()
            cities_serializer = CitySerializer(cities, many=True)
        return Response({"status": True, "cities": cities_serializer.data}, status=codes.OK)
            
class TrainingsAPI(APIView):
    def get(self, request):
        trainings = Trainings.objects.all()
        trainings_serializer = TrainingsSerializer(trainings, many=True)
        return Response({"status": True, "trainings": trainings_serializer.data}, status=codes.OK)