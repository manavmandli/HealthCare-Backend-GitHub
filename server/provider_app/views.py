from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from facility_app.models import *
from facility_app.serializers import *
from .utils import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from constants.status import codes
from common_app.models import *
from common_app.serializers import *


class ProviderView(APIView):

    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    profile = ProviderModel.objects.get(user=pk)
                else:
                    profile = ProviderModel.objects.get(user=request.user.id)
                serializer = ProviderSerializer(profile)
                return Response({"status":True, "message":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"User is not authenticated"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def post(self, request):
        try:
            user = request.user

            if user.is_authenticated and user.is_active:
               
                if ProviderModel.objects.filter(user=user).exists():
                    return Response({"status": False, "message": "provider already exist"}, status=codes.CONFLICT)

                serializer = ProviderSerializer(data=request.data)
           
                if serializer.is_valid():
                    serializer.save(user=user)
                    return Response({"status": True, "message": "provider profile added"}, status=codes.OK)
                else:
                    return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

    def patch(self, request):
        if request.user.is_authenticated and request.user.is_active:
            try:
                profile = ProviderModel.objects.get(user=request.user)
                serializer = ProviderSerializer(profile, data={**request.data, "user": request.user.id}, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True}, status=codes.OK)
                else:
                    return Response({'status': False, 'message': serializer.errors}, status=codes.SERVER_ERROR)
            except ProviderModel.DoesNotExist:
                return Response({'status': False, 'message': "Requested profile does not exist!"}, status=codes.CLIENT_ERROR)


class ProfilePictureAPI(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            picture = request.FILES.get('profile_picture')
            print(picture)
            try:
                old_profile_picture = ProfilePicturesModel.objects.get(user=request.user)                
                serializer = ProfilePictureSerializer(old_profile_picture, data={'profile_picture': picture}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Profile picture updated!"}, status=codes.OK)
                else:
                    return Response({"status": False, "message": serializer.errors}, status=codes.SERVER_ERROR)        
            except ProfilePicturesModel.DoesNotExist:
                serializer = ProfilePictureSerializer(data={'user': request.user.id, 'profile_picture': picture}) 
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response({"status": True, "message": "Profile picture updated!"}, status=codes.OK)
                else:
                    
                    return Response({"status": False, "message": serializer.errors}, status=codes.SERVER_ERROR)        
            except Exception as e:
                # from traceback import format_exc
                # print(format_exc(e))
                return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
        else:
            return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)

class ExperienceAPI(APIView):

    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    experience = ExperienceModel.objects.get(user=pk)
                else:
                    recordId = request.query_params.get('recordId')

                    if recordId is not None:

                        recordId = ExperienceModel.objects.get(id=recordId)

                        if recordId:

                            if request.user == recordId.user:
                        
                                serializer = ExperienceSerializer(recordId)
                                return Response({"status":True, "message":"Education details", "data":serializer.data}, status=codes.OK)
                            else:
                                return Response({"status":False, "message":"user not match"}, status=codes.AUTH_ERROR)

                    experience = ExperienceModel.objects.filter(user=request.user.id)
                serializer = ExperienceSerializer(experience, many=True)
                return Response({"status":True, "message":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"User is not authenticated"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def post(self, request):
        try:
            
            if request.user.is_authenticated and request.user.is_active:
              
                serializer = ExperienceSerializer(data=request.data)
                if serializer.is_valid():

                    serializer.save(user=request.user)
                    return Response({"status": True, "message": "Provider Experience added"}, status=codes.OK)
                else:
                    return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
            else:
                return Response({"status": False, "message": "Token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
        

    def patch(self, request, pk):
        try:
            id = pk 

            if request.user.is_authenticated and request.user.is_active:
                
                experience = ExperienceModel.objects.get(pk=id)

                serializer = ExperienceSerializer(experience, data=request.data, partial=True)

                if experience.user == request.user:
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status":True, "message":"Experience updated"}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
                else:
                    return Response({"status":False, "message":"Login user not match"}, status=codes.AUTH_ERROR)
                
            else:
                return Response({'status': False, 'message': 'Token is not valid'}, status=codes.CLIENT_ERROR)
        except ProviderModel.DoesNotExist:
            return Response({'status': False, 'message': 'Provider not found'}, status=codes.NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=codes.SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if request.user.is_authenticated and request.user.is_active:
                id = pk 
                experience = ExperienceModel.objects.get(id=pk)
                if request.user == experience.user:
                    experience.delete()
                    return Response({"status":True, "message":"Experience data deleted"}, status=codes.OK)
                else:
                    return Response({"status":False, "message":"user not match"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False,"message":"Please Login to access this resource."}, status=codes.CLIENT_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)
            

class EducationalView(APIView):

    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    education = EducationModel.objects.get(user=pk)
                else:
                    recordId = request.query_params.get('recordId')

                    if recordId is not None:

                        recordId = EducationModel.objects.get(id=recordId)

                        if recordId:

                            if request.user == recordId.user:
                        
                                serializer = EducationSerializer(recordId)
                                return Response({"status":True, "message":"Education details", "data":serializer.data}, status=codes.OK)
                            else:
                                return Response({"status":False, "message":"user not match"}, status=codes.AUTH_ERROR)

                    education = EducationModel.objects.filter(user=request.user.id)
                serializer = EducationSerializer(education, many=True)
                return Response({"status":True, "message":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"User is not authenticated"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)



    def post(self, request):
        try:
                
            if request.user.is_authenticated and request.user.is_active:

                serializer = EducationSerializer(data=request.data)
                                
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response({"status": True, "message": "user educational details added"}, status=codes.OK)
                else:
                    return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
            else:
                return Response({"status": False, "message": "Please login"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

        
    def patch(self, request, pk):
        try:
            
            id = pk 

            if request.user.is_authenticated and request.user.is_active:

                educational = EducationModel.objects.get(pk=id)

                serializer = EducationSerializer(educational, data=request.data, partial=True)

                if educational.user == request.user:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"status":True, "message":"Educational updated"}, status=codes.OK)

                    else:
                        return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
                else:
                    return Response({"status":False, "message":"login user not match"}, status=codes.AUTH_ERROR
                    )
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if request.user.is_authenticated and request.user.is_active:
                id = pk 
                education = EducationModel.objects.get(id=pk)
                if request.user == education.user:
                    education.delete()
                    return Response({"status":True, "message":"Educational data deleted"}, status=codes.OK)
                else:
                    return Response({"status":False, "message":"user not match"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False,"message":"Please Login to access this resource."}, status=codes.CLIENT_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)






class JobApplicationView(APIView):
    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    job_application = JobApplicationsModel.objects.get(user=pk)
                else:
                    orderId = request.query_params.get('orderId')

                    if orderId is not None:

                        orderId = JobApplicationsModel.objects.get(id=orderId)

                        if orderId:

                            if request.user == orderId.user:
                        
                                serializer = JobApplicationsSerializer(orderId)
                                return Response({"status":True, "message":"Job applicants details", "data":serializer.data}, status=codes.OK)
                            else:
                                return Response({"status":False, "message":"user not match"}, status=codes.AUTH_ERROR)

                    job_application = JobApplicationsModel.objects.filter(user=request.user.id)
                serializer = JobApplicationsSerializer(job_application, many=True)
                return Response({"status":True, "message":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"User is not authenticated"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)