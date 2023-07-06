from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from constants.status import codes
from provider_app.models import *
from provider_app.serializers import *
from .utils import *
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
                return Response({"status":True, "message":"City Displayed", "data":serializer.data}, status=codes.OK)
            else:
                city = CityModel.objects.all()
                serializer = CitySerializer(city, many=True)
                return Response({"status":True, "message":"Cities Displayed", "data":serializer.data}, status=codes.OK)
        except Exception as e:
            
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class FacilityAPI(APIView):
    def get(self, request, format=None):

        try:

            # if we have to view particular facility profile then this code of block will be used

            user = request.user
            if user.is_authenticated and user.is_active:
                current_facility = FacilityModel.objects.get(user_id=user.id)
                serializer = FacilitySerializer(current_facility)
                return Response({"status":True, "message":"Data displayed", "data":serializer.data}, status=codes.OK)

            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)


    def post(self, request):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                serializer = FacilitySerializer(data=request.data)
                if request.data.get("zipcode") == "":
                    return Response({"status":False, "message":"Zipcode may not be blank"})

                if request.data.get("phone_number") == "":
                    return Response({"status":False, "message":"Phone Number may not be blank"}, status=codes.CLIENT_ERROR) 

                documents_applicant = request.FILES.get("documents_applicant")

                if not documents_applicant:
                    return Response({"status":False, "message":"Document applicant may not be blank"}, status=codes.CLIENT_ERROR)

                if request.data.get("bank_account") == "":
                    return Response({"status":False, "message":"Bank Account may not be blank"}, status=codes.CLIENT_ERROR)

                if serializer.is_valid():
                    email = user.email
                    if FacilityModel.objects.filter(user_id__email=email).exists():
                        return Response({"status": False, "message": "Facility profile already exists"}, status=codes.CLIENT_ERROR)
                    serializer.save(user_id=user)
                    return Response({"status": True, "message": "Facility profile added"}, status=codes.OK)
                else:
                    return Response({"status": False, "message": serializer.errors}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status": False, "message": "Token is not set properly"}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
                
    def patch(self, request, pk, format=None):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:


                # if facility email and profile facility email will match then facility can update the profile


                id = pk 
                facility = FacilityModel.objects.get(pk=id)
                serializer = FacilitySerializer(facility, data=request.data,partial=True)

                user_name = facility.user_name

                user_id = facility.user_id

                facility_profile_email = FacilityModel.objects.get(user_id__email=user.email)

                facility_profile_email = facility_profile_email.user_id.email

                facility_profile_email = str(facility_profile_email)
                
                user_email = str(user)

                if user_email == facility_profile_email:
                    # Check if the bank account field is present in the request data
                    if 'bank_account' in request.data:
                        print("----------------")
                        # Check if the bank account has already been updated three times
                        if facility.bank_update_count >= 3:
                            return Response({"status":False, "message":"Facility you have reached the maximum number of bank account updates please talk to admin"}, status=codes.CLIENT_ERROR)
                        # Increase the bank_update_count by 1
                        facility.bank_update_count += 1
                        facility.save()

                    if serializer.is_valid():    
                        serializer.save(user_name=user_name, user_id=user_id)
                        return Response({"status":True, "message":"Facility profile updated"}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Facility profile not updated", "data":serializer.errors}, status=codes.CLIENT_ERROR)
                else:

                    # if facility email and profile facility email not match then it will display the message that user invalid action

                    return Response({"status":False, "message":"Facility invalid action"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
        
        except ObjectDoesNotExist as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
    
class SearchProviderAPI(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:

                # below code is for inserting the category filter, location filter, available filter and location filter

                category_id = request.query_params.get('category_filter')
                location_id = request.query_params.get('city_filter')
                available_id = request.query_params.get('available_filter')
                location_filter = request.query_params.get('location_filter')

                if category_id is not None:

                    # if i have to find provider as per category then it will display

                    category_filter = ProviderModel.objects.filter(category__title=category_id)

                    if category_filter:
                        serializer = ProviderSerializer(category_filter, many=True, context={'request': request})
                        return Response({"status":True, "message":"Category wise provider is displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Provider of this category not shown"}, status=codes.CLIENT_ERROR)
                
                elif location_id is not None:

                    # if i have to find provider as per city then it will display

                    city_filter = ProviderModel.objects.filter(city=location_id)

                    if city_filter:
                        serializer = ProviderSerializer(city_filter, many=True, context={'request': request})
                        return Response({"status":True, "message":"Location wise provider is displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Provider of this location not shown"}, status=codes.CLIENT_ERROR)
                    
                elif available_id is not None:

                    # if i have to find provider as per available then it will display

                    available_filter = ProviderModel.objects.filter(available=available_id)

                    if available_filter:
                        serializer = ProviderSerializer(available_filter, many=True, context={'request': request})
                        return Response({"status":True, "message":f"Provider {available_id}", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"provider of this search is not shown"}, status=codes.CLIENT_ERROR)
                    
                elif location_filter:
                    try:

                        # if i have to find provider as per nearest location then it will display

                        facility = FacilityModel.objects.get(user_id=location_filter)
                    except FacilityModel.DoesNotExist:
                        return Response({"status":False, "message":"Facility profile not found"}, status=status.HTTP_404_NOT_FOUND)

                    providers = ProviderModel.objects.filter(zipcode=facility.zipcode)
                    serializer = ProviderSerializer(providers, many=True)
                    return Response({"status":True, "message":"Nearby provider data displayed", "data":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)    

class HiringView(APIView):
    def post(self, request):
        try:
            serializer = HiringSerializer(data=request.data)
            user = request.user
            if user.role == "facility":

                # if facility have to send offer to provider then facility have to fill details like interview time, provider email, hourly rate and job open for

                if user.is_authenticated and user.is_active:
                    if serializer.is_valid():
                        user = request.user.id
                        facilityemail = FacilityModel.objects.get(user_id__id=user)
                        interview_time = serializer.validated_data['interview_time']
                        provideremail = serializer.validated_data["provider_email"]
                        hourly_rate = serializer.validated_data["hourly_rate"]
                        job_open_for = serializer.validated_data["job_open_for"]

                        # if provider email and facility email is match then it will display message that provider nd facility not be same
                        
                        if provideremail == facilityemail:
                            return Response({"status":True, "message":"Provider and Facility not be same", "data":serializer.errors}, status=codes.OK)
                        

                        new_data = HiringModel.objects.create(
                            provider_email=provideremail, facility_email=facilityemail, interview_time=interview_time,
                            hourly_rate=hourly_rate,
                            job_open_for=job_open_for,
                            status=False)
                        

                        # then email will send to provider that facility have make offer for you 
                        
                        new_data.save()
                        subject = 'Hiring Invitation'
                        message = f"Hello Provider I am Intrested to hiring {provideremail} because of your great qualities if you are intrested to doing this job interviewing time is {interview_time} '\n' Thanks Your Regards,{facilityemail}"
                        sendmail(subject, 'send_hiring_request', provideremail,
                                    {'message': message})
                        return Response({'status': True, 'message': "Hiring mail send succesfully"}, status=codes.OK)
                        
                    else:

                        # if hiring data is not fill proper as per form then it will give message that offer not send

                        return Response({"status":False,"message": "Offer not send ", "data":serializer.errors}, status=codes.SERVER_ERROR)
                else:
                    return Response({"status": False, "message": "Token is not set properly"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"This functionality is for facility"}, status=codes.AUTH_ERROR)
                
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def get(self, request, pk=None):
        try:
            id=pk
            if id is not None:
                return Response({"status":False, "message":'Enter valid details'}, status=codes.CLIENT_ERROR)

            user = request.user
            if user.role == "facility":

                # it will give data which facility have send offer to provider so facility can view the status of offer that the offer is accepted or not if offer is accepted the facility will get email

                if user.is_authenticated and user.is_active:
                    facility_id = request.user.id
                    email = FacilityModel.objects.get(user_id__id=facility_id)
                    hiringdata = HiringModel.objects.filter(facility_email=email)
                    serializer = HiringSerializer(hiringdata, many=True)
                    return Response({"status": True, "message": "All hiring data is displayed", "data": serializer.data}, status=codes.OK)
                else:
                    return Response({"status": False, "message": "Token is not set properly"}, status=codes.CLIENT_ERROR)
                
            if user.role == "provider":

                # it will give data of hiring so provider can view which faciltiy have request to them

                if user.is_authenticated and user.is_active:
                    provider_id = request.user.id
                    email = ProviderModel.objects.get(user_id__id=provider_id)
                    hiringdata = HiringModel.objects.filter(provider_email=email)
                    serializer = HiringSerializer(hiringdata, many=True)
                    return Response({"status": True, "message": "All hiring data is displayed", "data": serializer.data}, status=codes.OK)
                else:
                    return Response({"status": False, "message": "Token is not set properly"}, status=codes.CLIENT_ERROR)
                
            else:
                return Response({"status":False, "message":"This functionality is for provider and facility"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)


class WalletAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk 
        if id is not None:
            wallet = FacilityWalletModel.objects.get(id=id)
            serializer = FacilitySerializer(wallet)
            return Response({"status":True, "message":"Wallet is shown", "data":serializer.data}, status=codes.OK)
        else:
            wallet = FacilityWalletModel.objects.all()
            serializer = FacilitySerializer(wallet,many=True)
            return Response({"status":True, "message":"All wallet is shown", "data":serializer.data}, status=codes.OK)
        
    def post(self, request, pk=None, format=None):
        serializer = FacilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"New wallet is added"})
        else:
            return Response({"status":False, "message":"Wallet is not added"}, status=codes.CLIENT_ERROR)
        
    def patch(self, request, pk=None, format=None):
        ...

class AcceptsAppliedJobs(APIView):

    def get(self, request, format=None):

        try:

            user = request.user
            if user.is_authenticated and user.is_active:
                if user.role == "facility":
                    view_pending_job = JobApplications.objects.filter(facility_name__facility_id__user_id=user)
                    serializer = ApplyJobPostSerializer(view_pending_job, many=True)
                    return Response({"status":True, "message":"View pending jobs", "data":serializer.data}, status=codes.OK)
                else:
                    return Response({"status":False, "message":"This functionality is for facility"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
      

    def patch(self, request, pk, format=None):

        try:

            user = request.user
            id = pk 
            if user.is_authenticated and user.is_active:
                if user.role == "facility":
                    accepts_job_post = JobApplications.objects.get(pk=id)
                    cover_letter = accepts_job_post.cover_letter
                    user_id = accepts_job_post.user_id
                    facility_name = accepts_job_post.facility_name

                    serializer = ApplyJobPostSerializer(accepts_job_post, data=request.data, partial=True)

                    user = str(user)
                    
                    current_facility = JobApplications.objects.get(id=id)
                    current_facility_email = facility_name.facility_id.user_id.email

                    if user == current_facility_email:

                        if serializer.is_valid():
                            applied_job_status=serializer.validated_data["status"]
                            email = user_id

                            if applied_job_status == True:

                                subject = "Request accepted"
                                message_provider = f"{facility_name} so {user_id} your are selected congratulations"

                                sendmail(subject, 'accepted_job_request_mail_to_provider', email, {'message':message_provider})

                                message_facility = f"{request.user} you have accepted the request of {email}"

                                sendmail(subject,'accepted_job_request_mail_to_facility',request.user,{'message':message_facility})

                            else:

                                subject = "Request rejected"
                                message = f"{facility_name} so {user_id} you are not selected better luck next time"

                                sendmail(subject, 'rejected_job_request', email, {'message':message})

                            serializer.save(cover_letter=cover_letter, user_id=user_id, facility_name=facility_name)
                            return Response({"status":True, "message":"Accepted applied jobs", "data":serializer.data}, status=codes.OK)
                        else:
                            return Response({"status":False, "message":"Applied job not accepted"}, status=codes.CLIENT_ERROR)
                    else:
                        return Response({"status":False, "message":"Facility not matched"}, status=codes.AUTH_ERROR)
                else:
                    return Response({"status":False, "message":"This functionality is for facility"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
        
class ViewFacilityRating(APIView):
    def get(self, request, pk=None):

        try:

            user = request.user
            id = pk 
            if user.is_authenticated and user.is_active:
                if id is not None:
                    rating = ProviderRatingModel.objects.get(id=id)
                    serializer = ProviderRatingSerializer(rating)
                    return Response({"status":True, "message":"Provider rating found", "data":serializer.data}, status=codes.OK)
                else:
                    rating = ProviderRatingModel.objects.all()
                    serializer = RatingSerializer(rating, many=True)
                    return Response({"status":True, "message":"Provider rating found", "data":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"user please insert token or insert correct token"}, status=codes.CLIENT_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class GiveRatingToProvider(APIView):
    def post(self, request):

        try:

            user = request.user
            if user.role == "facility":
                if user.is_authenticated and user.is_active:
                    serializer = ProviderRatingSerializer(data=request.data)

                    get_facility_id = FacilityModel.objects.get(user_id=user)
                    
                    provider_exist = request.data["provider_id"]

                    facility_exist = request.data["facility_id"]

                    is_exist = ProviderRatingModel.objects.filter(facility_id=facility_exist, provider_id=provider_exist).exists()

                    if is_exist:
                        return Response({"status":False, "message":"Facility you can not give another rating to same provider"}, status=codes.CLIENT_ERROR)

                    

                    if serializer.is_valid():
                        serializer.save(facility_id=get_facility_id)
                        return Response({"status":True, "message":"Rating given to provider", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Please enter correct data", "data":serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"This functionality only for facility"}, status=codes.AUTH_ERROR)

        

        except ObjectDoesNotExist:
            return Response({"status":False, "message":"Invlaid provider selection"}, status=codes.CLIENT_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)