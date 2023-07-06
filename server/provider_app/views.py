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


# Create your views here.

class ProviderAPI(APIView):

    # if we have to view particular provider profile then this code of block will be used

    def get(self, request, pk=None, format=None):

        try:

            user = request.user
            if user.is_authenticated and user.is_active:
                if pk is not None:
                    provider = ProviderModel.objects.get(id=pk)
                    serializer = ProviderSerializer(provider, cotnext={'request':request})
                    return Response({"status":True, "message":"Provider displayed", "data":serializer.data}, status=codes.OK)
                else:

                    # if we have to see all the provider then this code of block will be used

                    providers = ProviderModel.objects.all()
                    serializer = ProviderSerializer(providers, many=True, context={'request':request})
                    return Response({"status":True, "message":"Providers displayed", "data":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"Token is not set properly"})

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)    


    def post(self, request):

        # This functionality is used to post the prfoile of provider
        user =request.user
        if user.is_authenticated and user.is_active:
            serializer = ProviderSerializer(data=request.data)
            if serializer.is_valid():

                try:


                    print("--------------- USER : ",user)
                    print("--------------- USER TYPE : ",type(user))

                    # it will take all the 37 field which is given in the documents


                    # the user_id field is there because if the current user data will be store in that so another user will not fill the profile other user
                    
                    
                    user_id = serializer.validated_data["user_id"]
                    
                    # category filed is there to store which user is belong to which category 

                    print("--------------- USER ID : ",user_id)

                    provider = ProviderModel.objects.get(user_id__email=user)
                    print("------------ PROVIDER : ",provider)
                    provider_name = provider.user_id.email


                    if str(user_id) == str(provider_name):
                        return Response({"status":False, "message":"User profile already exist"}, status=codes.CLIENT_ERROR)

                except ObjectDoesNotExist:

                    category = serializer.validated_data["category"]
                    
                    # it will check if npdb have data or not
                    
                    npdb = serializer.validated_data["npdb"]

                    # it will check if peer attestation have data or not

                    peer_attestation_form = serializer.validated_data["peer_attestation_form"]

                    # it will check if cpr certification have data or not
                    
                    cpr_certification = serializer.validated_data["cpr_certification"]


                    if user_id == user:
                        if str(category) == "MD":

                            # it will check if provider category is MD or not
                    
                            if npdb!=None:


                                # npdb form is there because if MD category user is there then it will fill the npdb details form and other category user is there then it will not fill the npdb field
                                
                                
                                serializer.save(npdb=npdb, peer_attestation_form="", cpr_certification="",category=user.eligible_service)
                                return Response({"status":True, "message":"Provider profile added"}, status=codes.OK)
                            else:

                                # if MD will not fill the form of npdb then the message will display that MD must fill form of npdb

                                return Response({"status":False, "message":"MD must fill form of npdb"}, status=codes.CLIENT_ERROR)
                            
                        if str(category) == "Medical Director":
                            
                            # it will check if provider category is Medical Director or not

                            if peer_attestation_form!=None:
                                
                                
                                # peer attestation form is there because if Medical Director category user is there then it will fill the peer attestation details form and other category user is there then it will not fill the peer attestation field



                                serializer.save(peer_attestation_form=peer_attestation_form, npdb="", cpr_certification="", category=user.eligible_service)
                                return Response({"status":True, "message":"Provider profile added"}, status=codes.OK)
                            else:

                                # if Medical Director will not fill the form of peer attestation then the message will display that Medical Director must fill form of peer attestation 


                                return Response({"status":False, "message":"Medical Director must fill form of peer attestation"})
                            
                        if str(category) == "BHT/ Medical Staff":
                            
                            # it will check if provider category is BHT/ Medical Staff or not

                            if cpr_certification!=None:


                                # cpr certification form is there because if BHT/ Medical staff is there then it will fill the cpr_certification details form  and other category user is there then it will not fill the cpr certification field


                                serializer.save(cpr_certification=cpr_certification, npdb="", peer_attestation_form="", category=user.eligible_service)
                                return Response({"status":True, "message":"Provider profile added"}, status=codes.OK)
                            else:

                                # if BHT/ Medical will not fill the form of cpr certification then the message will display that BHT/ Medical must fill form of cpr certification

                                return Response({"status":False, "message":"BHT/ Medical Staff must fill form of cpr certification"})
                        else:

                            # if provider is not belong to MD, Medical Director and BHT/ Medical then provider can not fill this field and all other documents user can fill

                            serializer.save(cpr_certification="", npdb="", peer_attestation_form="",category=user.eligible_service)
                            return Response({"status":True, "message":"Provider profile added", "data":serializer.data}, status=codes.OK)

                    else:

                        # it will show message if user will post other profile user can only post their profile

                        return Response({"status":False, "message":"You can only post your profile"}, status=codes.AUTH_ERROR)
                else:
                    return Response({"status":False, "message":str(serializer.errors)}, status=codes.CLIENT_ERROR)
            else:
                # if facility will not fill data as per the field then it will display message that profile not added

                errors = serializer.errors
                first_field = list(errors.keys())[0]
                first_error_message = errors[first_field][0]

                error_message = f"{first_field}: {first_error_message}"
                return Response({"status": False, "message": error_message}, status=codes.CLIENT_ERROR)
        else:
            return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)
        
       
        
    def patch(self, request, pk, format=None):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                id = pk

                # Get the current provider
                provider = ProviderModel.objects.get(pk=id)
                serializer = ProviderSerializer(provider, data=request.data, partial=True)

                user_email = str(user.email)
                print("----------- USER EMAIL : ",user_email)
                print("----------- USER EMAIL TYPE : ",type(user_email))

                print("--------------- PROVIDER EMAIL : ",provider.user_id.email)

                print(user_email==str(provider.user_id.email))


                # If the current user and provider profile email match, allow profile update
                if user_email == str(provider.user_id.email):
                    # Check if the bank account field is present in the request data
                    if 'bank_account' in request.data:
                        # Check if the bank account has already been updated three times
                        if provider.bank_update_count >= 3:
                            return Response({
                                "status": False,
                                "message": "Proiver you have reached the maximum number of bank account updates please talk to admin"
                            }, status=codes.CLIENT_ERROR)
                        # Increase the bank_update_count by 1
                        provider.bank_update_count += 1
                        provider.save()

                    if serializer.is_valid():
                        serializer.save(
                            category=user.eligible_service,
                            user_name=provider.user_name
                        )

                        return Response({
                            "status": True,
                            "message": "Profile updated",
                            "data": serializer.data
                        }, status=codes.OK)
                    else:
                        return Response({
                            "status": False,
                            "message": "Invalid user action",
                            "data": serializer.errors
                        }, status=codes.CLIENT_ERROR)
                else:
                    return Response({
                        "status": False,
                        "message": "Invalid user action"
                    }, status=codes.CLIENT_ERROR)
            else:
                return Response({
                    "status": False,
                    "message": "Token is not set properly"
                })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=codes.CLIENT_ERROR)

class SearchFacilityAPI(APIView):
    def get(self, request, format=None):

        try:

            user = request.user
            if user.is_authenticated and user.is_active:

                # below code is for inserting the location filter, facility filter, job filter keyword and credenntial

                location_id = request.query_params.get('location_filter')
                facility_id = request.query_params.get('facility_filter')
                job_filter_keyword_id = request.query_params.get('job_filter_keyword')
                credential_id = request.query_params.get('credential_filter')

                if location_id is not None:

                    # if i have to find job as per location then it will display

                    location_filter = FacilityModel.objects.filter(city=location_id)

                    if location_filter:
                        serializer = FacilitySerializer(location_filter, many=True)
                        return Response({"status":True, "message":"Location wise facility displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Facility of this location is not displayed"}, status=codes.CLIENT_ERROR)
                    
                elif facility_id is not None:

                    # if i have to find job as per facility then it will display

                    facility_filter = FacilityModel.objects.filter(facility_name=facility_id)

                    if facility_filter:
                        serializer = FacilitySerializer(facility_filter, many=True)
                        return Response({"status":True, "message":"Facility displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"facility not displayed"})
                                    
                elif job_filter_keyword_id is not None:

                    # if i have to find job as per any keyword of job then it will display

                    job_filter_keyword = JobPostModel.objects.filter(job_filter__icontains=job_filter_keyword_id)

                    if job_filter_keyword:
                        serializer = JobPostSerializer(job_filter_keyword, many=True)
                        return Response({"status":True, "message":"Filter job with relevant keyword is displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Filter job with relevant keyword is not displayed"}, status=codes.CLIENT_ERROR)
                    
                elif credential_id is not None:

                    # if i have to find job as per credential then it will display

                    credential_filter = JobPostModel.objects.filter(credentials__icontains=credential_id)

                    if credential_filter:
                        serializer = JobPostSerializer(credential_filter, many=True)
                        return Response({"status":True, "message":"Filter with credentials is displayed", "data":serializer.data}, status=codes.OK)
                    else:
                        return Response({"status":False, "message":"Filter credentials is not available"})

                else:

                    # if i am not applying any filter then all jobs will display

                    job_post = JobPostModel.objects.all()
                    serializer = JobPostSerializer(job_post, many=True)
                    return Response({"status":True, "message":"All job post are displayed", "data":serializer.data}, status=codes.OK)

            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
        

class AcceptHiring(APIView):
    def patch(self,request,pk,format=None):

        try:


            # if facility have offer to provider then if provider have to accpet the facility offer for job then provider can accept from here 


            user = request.user
            if user.role == "provider":
                id = pk 
                if user.is_authenticated and user.is_active:
                    hire = HiringModel.objects.get(pk=id)
                    provideremail = request.user.id
                    serializer = HiringSerializer(hire,data=request.data)

                    provider_email = ProviderModel.objects.get(user_id__id=provideremail)

                    facility_email = hire.facility_email

                    facility_send_email = hire.facility_email.user_id.email

                    if serializer.is_valid():
                        subject = "Provider accept request"
                        message = ""
                        sendmail(subject, 'accept_hiring_mail', facility_send_email,
                                    {'message': message})
                        serializer.save(provider_email=provider_email,facility_email=facility_email)
                        return Response({'status': True,'message': 'status updated succesfully', 'data': serializer.data}, status=codes.OK)
                    else:
                        return Response({'status': False, 'message': 'Fill data properly', 'data': serializer.errors}, status=codes.CLIENT_ERROR)
                else:
                    return Response({"status": False, "message": "Token is not set properly"})
            else:
                return Response({"status":False, "message":"This functionality is for provider"}, status=codes.AUTH_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
        
class ViewProviderRating(APIView):
    def get(self, request, pk=None):
        try:
            user = request.user
            id = pk 
            if user.is_authenticated and user.is_active:
                if id is not None:
                    rating = ProviderRatingModel.objects.get(id=id)
                    serializer = ProviderRatingSerializer(rating)
                    return Response({"status":True, "message":"Facility rating displayed", "data":serializer.data}, status=codes.OK)
                else:
                    rating = ProviderRatingModel.objects.all()
                    serializer = ProviderRatingSerializer(rating, many=True)
                    return Response({"status":True, "message":"Facilites rating displayed", "data":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class AverageRatingProvider(APIView):
    def get(self, request, pk=None):
        try:
            user = request.user
            id = pk 
            if user.is_authenticated and user.is_active:
                if id is not None:
                    rating = ProviderAverageRatingModel.objects.get(id=id)
                    serializer = ProviderTotalRatingSerializer(rating)
                    return Response({"status":True, "message":"Facility rating displayed", "data":serializer.data}, status=codes.OK)
                else:
                    rating = ProviderAverageRatingModel.objects.all()
                    serializer = ProviderTotalRatingSerializer(rating, many=True)
                    return Response({"status":True, "message":"Facilites rating displayed", "data":serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
   
class GiveRatingToFacility(APIView):
    def post(self, request):
        try:
            user = request.user
            if user.role == "provider":
                if user.is_authenticated and user.is_active:
                    serializer = ProviderRatingSerializer(data=request.data)

                    get_provider_id = ProviderModel.objects.get(user_id=user)

                    facility_exist = request.data["facility_id"]

                    facility_exist = str(facility_exist)

                    provider_exist = str(get_provider_id.id)

                    is_exist = ProviderRatingModel.objects.filter(provider_id=provider_exist, facility_id=facility_exist).exists()

                    if is_exist:
                        return Response({"status":False, "message":"Provider you can not give another rating to same Facility"}, status=codes.CLIENT_ERROR)
                    
                    if serializer.is_valid():
                        serializer.save(provider_id=get_provider_id)
                        return Response({"status":True, "message":"Rating given to facility", "data":serializer.data}, status=codes.OK)
                    else:
                        errors = serializer.errors
                        custom_errors = {}
                        for field, field_errors in errors.items():
                            if field == "facility_id":
                                custom_errors[field] = ["The selected facility does not exist."]
                                return Response({"status":False, "message":"Validation error", "errors":custom_errors}, status=codes.CLIENT_ERROR)

                else:
                    return Response({"status":False, "message":"Token is not set properly"}, status=codes.AUTH_ERROR)
            else:
                return Response({"status":False, "message":"This functionality only for provider"}, status=codes.AUTH_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)