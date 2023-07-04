from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from provider_app.models import *
from provider_app.serializers import *
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from urllib.error import HTTPError
from constants.status import codes
from django.db.models import Q

# Create your views here.


class FacilityProfileView(APIView):
    def post(self, request):
        try:
            user = request.user
            required_fields = {'facility_name', 'documents_applicant', 'professional_information', 'achivements_info'}
            if user.is_authenticated and user.is_active:
                for field in required_fields:
                    if field not in request.data:
                        return Response({"status":False, "message":"all fields must be required"}, status=codes.CLIENT_ERROR)
                request.data['user'] = user.id
                serializer = FacilitySerializer(data=request.data)
                if serializer.is_valid():
                    email = user.email
                    if FacilityModel.objects.filter(user__email=email).exists():
                        return Response({"status":False, "message":"user profile already exists"}, status=codes.CONFLICT)
                    serializer.save()
                    return Response({"status":True, "message":"Facility profile added"}, status=codes.OK)
                else:
                    # Return error message for serializer errors
                    error_message = "Invalid data provide. Please check the following errors:"
                    errors = []
                    for field, field_errors in serializer.errors.items():
                        field_errors = [str(error) for error in field_errors]
                        errors.append(f"{field} : {', '.join(field_errors)}")
                    return Response({"status":False, "message":serializer.errors}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False, "message":"Authentication token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)




class JobPostAPI(APIView):
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                job_post = JobPostModel.objects.get(id=pk)
                serializer = FacilityJobPostingSerializer(job_post)
                return Response({"status": True, "jobs": serializer.data}, status=codes.OK)
            else:
                title = request.GET.get('title')
                if request.user.role == "provider":
                    job_post = JobPostModel.objects.filter(Q(title__icontains=title) if title else Q()).order_by('-posted_on')
                    serializer = ProviderJobPostingSerializer(job_post, many=True)
                    return Response({"status": True, "jobs": serializer.data}, status=codes.OK)

                elif request.user.role == "facility":
                    job_post = JobPostModel.objects.filter(Q(user=request.user) & Q(title__icontains=title) if title else Q())
                    serializer = FacilityJobPostingSerializer(job_post, many=True)
                    return Response({"status": True, "jobs": serializer.data}, status=codes.OK)

        except JobPostModel.DoesNotExist:
            return Response({"status": False, "message": "Requested job post does not exist!"}, status=codes.CLIENT_ERROR)

        except Exception as e:
            print(e)
            return Response({"status": False, "message": str(e)}, status=codes.CLIENT_ERROR)
        
    def patch(self, request, pk, format=None):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                id = pk 
                job_post = JobPostModel.objects.get(pk=id)
                if job_post.user_id == user:
                    serializer = JobPostSerializer(job_post, data=request.data, partial=True)
                    if serializer.is_valid():
                        facility_name = FacilityModel.objects.get(user_id=user.id)
                        serializer.save(user_id=user, facility_id=facility_name)
                        return Response({"status":True, "message":"Job post updated", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Job post not updated", "data":serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status":False, "message":"Facility is not authorized to update this job post"}, status=codes.CONFLICT)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)
