from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from .models import *
from .serializers import *
from .paginators import *
from constants.status import codes
from utils.notifications import send_notification

# Create your views here.
class JobFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    city = filters.CharFilter(field_name="city", lookup_expr="in")
    
    class Meta:
        model = JobPostModel
        fields = "__all__"
        
class JobPostAPI(APIView, JobListPagination):
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                job_post = JobPostModel.objects.get(id=pk)
                if request.user.role == "facility":
                    serializer = FacilityJobPostSerializer(job_post)
                else:
                    serializer = ProviderJobPostSerializer(job_post)
                return Response({"status":True, "jobs": serializer.data}, status=codes.OK)
            else:
                if request.user.role == "provider":
                    if request.query_params:
                        open_job_posts = JobPostModel.objects.filter(job_status=0)
                        filtered_job_posts = JobFilter(request.GET, queryset=open_job_posts)
                        paginated_job_posts = self.paginate_queryset(filtered_job_posts.qs, request, view=self)
                        serializer = ProviderJobPostSerializer(paginated_job_posts, many=True)
                        return Response({"status":True, "jobs": serializer.data, "page_count": self.get_paginated_response(serializer.data).data.get('total_pages')}, status=codes.OK)
                    else:
                        open_job_posts = JobPostModel.objects.filter(job_status=0)
                        paginated_job_posts = self.paginate_queryset(open_job_posts, request, view=self)
                        serializer = ProviderJobPostSerializer(paginated_job_posts, many=True)
                        return Response({"status":True, "jobs": serializer.data, "page_count": self.get_paginated_response(serializer.data).data.get('total_pages')}, status=codes.OK)
                else:
                    job_posts = JobPostModel.objects.filter(user=request.user)
                    serializer = FacilityJobPostSerializer(job_posts, many=True)
                    return Response({"status":True, "jobs": serializer.data}, status=codes.OK)
        except JobPostModel.DoesNotExist:
            return Response({"status":False, "message": "Requested job post does not exist!"}, status=codes.CLIENT_ERROR)

        except Exception as e:
            print(e)
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def post(self, request, format=None):
        try:
            user = request.user
            # in this functionality, facility can post the job
            if user.role == "facility":
                if user.is_authenticated and user.is_active:
                    if request.data.get('from_datetime') > request.data.get('to_datetime'):
                        return Response({"status":False, "message":"Please select appropiate date."}, status=codes.CLIENT_ERROR)
                    serializer = JobPostSerializer(data={**request.data, "user":user.id})
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status":True, "message": "Your job has been posted!"}, status=codes.OK)
                    else:
                        return Response({"status":False, "message": serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status":False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False, "message": "Forbidden"}, status=codes.FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"status":False, "message": str(e)}, status=codes.SERVER_ERROR)
        
    #TODO : Update function    
        
    # def patch(self, request, pk, format=None):
    #     try:
    #         user = request.user
    #         if user.role == "facility":
    #             if user.is_authenticated and user.is_active:
    #                 id = pk 
    #                 job_post = JobPostModel.objects.get(pk=id)
    #                 if job_post.user_id == user:  # check if the job post was created by the current user
    #                     serializer = JobPostSerializer(job_post, data=request.data, partial=True)
    #                     if serializer.is_valid():
    #                         facility_name = FacilityModel.objects.get(user_id=user.id)
    #                         serializer.save(user_id=user, facility_id=facility_name)
    #                         return Response({"status":True, "message":"Job post updated", "data":serializer.data}, status=codes.OK)
    #                     else:
    #                         return Response({"status":False, "message":"Job post not updated", "data":serializer.errors}, status=codes.CLIENT_ERROR)
    #                 else:
    #                     return Response({"status":False, "message":"Facility is not authorized to update this job post"}, status=codes.AUTH_ERROR)
    #             else:
    #             else:
    #                 return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
    #         else:
    #             return Response({"status":False, "message":"This functionality is for facility"}, status=codes.CLIENT_ERROR)

    #     except Exception as e:
    #         return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)


    def patch(self, request, pk, format=None):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                id = pk 
                job_post = JobPostModel.objects.get(pk=id)
                if job_post.user == user:
                    serializer = JobPostSerializer(job_post, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status":True, "message":"Job post updated"}, status=codes.OK)
                    else:
                        return Response({"status":False, "message": serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status":False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)

class JobApplicationsAPI(APIView):
    def get(self, request, pk=None, format=None):
        # it will display which provider have already applied jobs to view status of job
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                id = pk 
                if id is not None:
                    job_application = JobApplications.objects.get(id=id)
                    serializer = JobApplicationsSerializer(job_application)
                    return Response({"status":True, "applications":serializer.data}, status=codes.OK)
                else:
                    job_applications = JobApplications.objects.filter(user=request.user)
                    serializer = UserJobApplicationsSerializer(job_applications, many=True)
                    return Response({"status":True, "applications":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message": "Unauthorized"}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            print(e)
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
        
    def post(self, request, pk=None, format=None):

        # provider will apply job in which provider is eligible for
        try:
            user = request.user
            if user.role == "provider":
                if user.is_authenticated and user.is_active:
                    serializer = JobApplicationsSerializer(data={**request.data, "user": user.id})
                    if serializer.is_valid():
                        serializer.save()
                        sent = send_notification(reciever=serializer.validated_data['job'].user, action="new_job_application", context=[serializer.validated_data['job'].title])
                        return Response({"status":True, "message":"Application successful!"}, status=codes.OK)
                    else:
                        return Response({"status":False, "message": serializer.errors}, status=codes.SERVER_ERROR)
                else:
                    return Response({"status":False, "message": "Unauthorized"}, status=codes.FORBIDDEN)
            else:
                return Response({"status":False, "message":"This functionality is for provider"}, status=codes.OK)
            # else:
            #     return Response({"status":False, "message": "Verification is required in order to apply for this job!"}, status=codes.AUTH_ERROR)

        except Exception as e:
            print(e)
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)
        
    def patch(self, request, pk=None):
        try:
            if request.user.is_authenticated and request.user.is_active:
                job_instance = JobApplications.objects.get(id=pk)
                if job_instance.job.user == request.user or job_instance.user == request.user:
                    serializer = JobApplicationsSerializer(job_instance, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        print(serializer.validated_data)
                        if serializer.validated_data.get('status') == 0:
                            sent = send_notification(reciever=job_instance.user, action="new_hiring_offer", context=[job_instance.job.user.__str__()])
                        if serializer.validated_data.get('status') == 2:
                            sent = send_notification(reciever=job_instance.job.user, action="accept_hiring_offer", context=[job_instance.user.__str__()])
                        if serializer.validated_data.get('status') == 3:
                            sent = send_notification(reciever=job_instance.job.user, action="reject_hiring_offer", context=[job_instance.user.__str__()])
                        return Response({"status": True, "message": "Job application updated!"}, status=codes.OK)
                    else:
                        return Response({"status": False, "message": serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        except JobApplications.DoesNotExist:
            return Response({"status": False, "message": "Invalid job application!"}, status=codes.CLIENT_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)