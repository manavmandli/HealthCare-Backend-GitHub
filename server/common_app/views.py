from django.shortcuts import render
from .models import * 
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from provider_app.models import *
from provider_app.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from urllib.error import HTTPError

# Create your views here.


class Cities(APIView):
    def get(self, request, pk=None,format=None):
        try:
            id = pk
            if id is not None:
                city = CityModel.objects.get(id=id)
                serializer = CitySerializer(city)
                return Response({"status":True, "message":"City Displayed", "data":serializer.data}, status=status.HTTP_200_OK)
            else:
                city = CityModel.objects.all()
                serializer = CitySerializer(city, many=True)
                return Response({"status":True, "message":"Cities Displayed", "data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"status":False, "message":str(e)}, status=status.HTTP_400_BAD_REQUEST)