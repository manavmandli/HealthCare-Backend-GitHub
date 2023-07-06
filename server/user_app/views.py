from .models import *
from utils.mail_helpers import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import status
from facility_app.models import *
from provider_app.models import *
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from constants.status import codes
from constants.project import PASSWORD_RESET_LINK_EXPIRY_MINS
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

# def get_time_difference(dt1, dt2=None, from_now=False):
#     if from_now:
#         return timezone.now() - dt1
#     else:
#         return dt1 - dt2   

class UserRegistrationView(APIView):
    def post(self, request):
        try:
            required_fields = {"email", "role", "first_name", "last_name", "password", "confirm_password"}
            for field in required_fields:
                if field not in request.data:
                    if field == "confirm_password":
                        return Response({"status": False, "message": "Please enter password!"}, status=codes.CLIENT_ERROR)
                    else:
                        return Response({"status": False, "message": f"Please enter {field.replace('_', ' ')}!"}, status=codes.CLIENT_ERROR)
            else:
                email = request.data.get("email")
                role = request.data.get("role")
                first_name = request.data.get("first_name")
                last_name = request.data.get("last_name")
                
                if CustomUser.objects.filter(email=email).exists():
                    return Response({"status": False, "message": "An account with this email already exists!"}, status=codes.CLIENT_ERROR)
                else:
                    password = request.data.get('password')
                    confirm_password = request.data.get('confirm_password')
                    if password == confirm_password:
                        if role in dict(ROLE_STATUS.choices).keys():
                            created_user = CustomUser.objects.create_user(email=email, role=role, first_name=first_name, last_name=last_name, password=password)
                            if created_user:
                                link = RegistrationLinkModel.objects.create(user_id=created_user)
                                subject = 'Activate your account'
                                message = f'{request.build_absolute_uri(reverse("activate", args=[link.reset_uuid]))}\n\nThanks,\nThe Team'
                                # send_template_mail(subject=subject, to=email, context=  {'message': message, 'firstname': created_user.first_name}, template='confirmation_link')
                                return Response({"status":True, "message":"mail send succesfully"}, status=codes.OK)
                        else:            
                            return Response({"status": False, "message": "Invalid role"}, status=codes.CLIENT_ERROR)
                    else:
                        return Response({"status": False, "message": "Passwords do not match!"}, status=codes.CLIENT_ERROR)
        except AttributeError as e:
            error_message = str(e)  # Convert the exception to a string
            return Response({"status": False, "message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateView(APIView):
    def get(self, request, reset_uuid):
        try:
            # Retrieve the registration link from the database
            link = RegistrationLinkModel.objects.get(reset_uuid=reset_uuid)
            user = link.user_id
            # if user will not click the link in 5 minutes then link will be expired
            if link.created_at > timezone.now()-timezone.timedelta(minutes=PASSWORD_RESET_LINK_EXPIRY_MINS):
                if user.is_active == False:
                    link.delete()        
                return Response({"status":False, "message":"Link is expired please try again"}, status=codes.CLIENT_ERROR)
            else:
                # Activate the user account
                user.is_active = True

        except RegistrationLinkModel.DoesNotExist:
            return Response({'status':False, 'message':'activate_error'}, status=codes.CLIENT_ERROR)       
        
        
    

        # if user will click link in 5 minutes then user will be activate and user will get message that your account is activate


        subject = 'Account Activated'
        send_template_mail(subject=subject, to=user, template_name='confirmed_link')
        user.save()
        
        return Response({'status':True,'message':'Activate Done'}, status=status.HTTP_200_OK)

class UserLoginView(APIView):


    # it will give details of user data which is store in Custom User model
    

    def get(self, request, pk=None, format=None):

        try:

            id = pk 

            # if we have to view particular user data then we can view 

            if id is not None:
                user = CustomUser.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response({"status":True, "message":"User is displayed", "data":serializer.data}, status=status.HTTP_200_OK)
            else:


                # if we have to view all user data at a one time then we can view


                user = CustomUser.objects.all()
                serializer = UserSerializer(user, many=True)
                return Response({"status":True, "message":"All user are displayed", "data":serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":False, "message":e}, status=codes.CLIENT_ERROR)


    def post(self, request):

            # it will ask to fill details of email and password at a login time


            email = request.data.get("email")
            password = request.data.get("password")


            # if email and password data will be blank then it will give message to fill details of email and password


            if email is None:
                return Response({'status':False,'message': 'Please provide email!'}, status=codes.CLIENT_ERROR)


            if password is None:
                return Response({"status":False, "message":"Please provide password!"}, status=codes.CLIENT_ERROR)
            

            # it will check in databse if email and password is wrong then it will give message that invalid email or password

            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active:
                    if user.check_password(password):
                        
                        # If password matches for the user, start a session for the user by logging them in
                        login(request, user)
                        
                        # After starting the session, get user's authentication token or create one if it is not yet generated
                        token, _ = Token.objects.get_or_create(user=user)
                        is_profile_created = BaseProfileModel.objects.filter(user=user).exists()
                        return Response({"status": True, "token": token.key, "createdProfile": is_profile_created, "userData": {"first_name": user.first_name, "last_name": user.last_name, "role": user.role}, 'message': 'Logged in succesfully!'}, status=codes.OK)    
                    else:
                        return Response({'status':False,'message': 'Invalid password!'},status=codes.CLIENT_ERROR)
                else:
                    return Response({'status':False,'message': 'Account is disabled'}, status=codes.CLIENT_ERROR)

            # if user is not active then it will display message that account is disabled
            except CustomUser.DoesNotExist:
                return Response({'status':False, 'message': 'Invalid credentials!'},status=codes.CLIENT_ERROR)
            except ValidationError as valError:
                # print(valError)
                return Response({'status':False,'message': str(valError)},status=codes.CLIENT_ERROR)
            except Exception as e:
                return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class ChangePassword(APIView):
    def post(self, request):

        try:

            user = request.user
            if user.is_authenticated and user.is_active:

                # if user is authenticated and user is active then user have permission to change password functionality

                serializer = ChangePasswordSerializer(data=request.data)
                if serializer.is_valid():


                    # if old password and new password is matching then user will able to change old password


                    old_password = serializer.data.get('old_password')
                    new_password = serializer.data.get('new_password')

                    validate_password(request.data['new_password'])
                    
                    

                    if user.check_password(old_password):
                        user.set_password(new_password)


                        # it will save a new password in user account and user will have to login with that new password


                        user.save()

                        # it will give message that password updated successfully to user

                        return Response({'status':True, 'data':serializer.data, 'message': 'Password updated succesfully'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':False,'message': 'Incorrect old password', 'data':serializer.errors}, status=codes.CLIENT_ERROR)
                else:

                    # if user will not fill proper details then user get message that fill data properly

                    return Response({'status':False,'message': 'Fill data properly', 'data':serializer.errors}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message": "Token is not set properly"})

        except ValidationError as e:
            return Response({"status": False, "message": str(e)}, status=codes.CLIENT_ERROR)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class ResetPasswordSendLinkView(APIView):
 
    def post(self, request, format=None):

        if request.data.get("email") is None:
            return Response({"status":False, "message": "Email must be selected"}, status=codes.CLIENT_ERROR)

        if CustomUser.DoesNotExist:
            return Response({"status":False, "message":"Email must be correct"}, status=codes.CLIENT_ERROR)

        try:


            # it will ask to fill detail of email

            if request.data.get("email") == "":
                return Response({"status":False, "message":"Email must be entered"}, status=codes.CLIENT_ERROR)

            email = request.data.get('email')


            get_user = CustomUser.objects.get(email=email)

            


            # if email is true then it will create link in password reset link model


            new_reset_obj = PasswordResetLinkModel.objects.create(user=get_user)

            reset_uuid = new_reset_obj


            # it will send mail that password reset link is send please click to reset password


            subject = 'Reset Password'
            
            message = request.build_absolute_uri(reverse("reset-password", args=[reset_uuid]))

            send_template_mail(subject, 'reset_password_link', email, {'message':message})
            
            return Response({'status':True,'message':"A password reset link has been sent to your registred email!"}, status=status.HTTP_200_OK)
            
        except Exception as e:


            # if user will do any mistake then user will get message to related that


            return Response({'status':False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except CustomUser.DoesNotExist:


            # if user email is not in database then user will get message that given email is not registered


            return Response({'message':"Given email is not registered!"}, status=codes.CLIENT_ERROR)
    
class ResetPasswordFormView(APIView):
    def post(self, request, uu_id=uuid4(), format=None):

        # this step will come after user will click on the link which is send for reset password

        try:
        
            # it will ask to fill details of new password and confirm paswword

            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            validate_password(request.data['new_password'])


            # if user will blank the field of new password then it will display the message that new password fill is required


            if new_password is None:
                return Response({'status':False,"message":"New password field is required."}, status=codes.CLIENT_ERROR)
            
            # if user will blank the field of confirm password then it will display the message that confirm password fill is required
            
            if confirm_password is None:
                return Response({'status':False,"message":"Confirm password field is required."}, status=codes.CLIENT_ERROR)

            if new_password == "":
                return Response({'status':False,"message":"you can not keep new password blank."}, status=codes.CLIENT_ERROR)

            if confirm_password == "":
                return Response({'status':False,"message":"you can not keep confirm password blank."}, status=codes.CLIENT_ERROR)
            
            if new_password == confirm_password:

                # if new password and confirm password is match then password will change and user will login with that password

                try:

                    get_user = PasswordResetLinkModel.objects.get(reset_uuid=uu_id).user
                    get_user.password = make_password(new_password)
                    get_user.save()
                    return Response({'status':True,'message':'Password successfully reset. you can login now'}, status=status.HTTP_200_OK)
                
                except PasswordResetLinkModel.DoesNotExist:
                    return Response({"status": False, "message": "Invalid URL"}, status=codes.CLIENT_ERROR) 
            else:

                # if password details will not fill proper then it will give message that password does not match

                return Response({'status':False,'message':'New Password and Confirm password does not match'}, status=codes.CLIENT_ERROR)

        except ValidationError as e:
            return Response({"status": False, "message": str(e)}, status=codes.CLIENT_ERROR)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

class BaseProfileAPI(APIView):
    def get(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                if pk is not None:
                    base_profile = BaseProfileModel.objects.get(user__id=pk)
                else:
                    base_profile = BaseProfileModel.objects.get(user__id=request.user.id)
                base_profile_serializer = BaseProfileSerializer(base_profile, context={"request": request})
                return Response({"status": True, "base_profile": base_profile_serializer.data}, status=status.HTTP_200_OK)
            except BaseProfileModel.DoesNotExist:
                return Response({"status": False, "message": "Requested BaseProfile record does not exist"}, status=status.HTTP_200_OK)
        else:
            raise PermissionError()   
    
    def post(self, request):
        contact_number = request.data.get('contact_number')
        if contact_number is not None:
            contact_no = PhoneNumber.from_string(contact_number)
            whatsapp_number = request.data.get('whatsapp_number')
            if whatsapp_number is not None:
                whatsapp_number = str(PhoneNumber.from_string(whatsapp_number).as_e164) 
            base_serializer = BaseProfileSerializer(data={**request.data, "user": request.user.id, "contact_number": str(contact_no), whatsapp_number: whatsapp_number})
            if base_serializer.is_valid():
                base_serializer.save()
                return Response({"status": True, "message": "Your profile has been saved!"}, status=codes.OK)
            else:
                return Response({"status": False, "message": str(base_serializer.errors)}, status=codes.CLIENT_ERROR)
        else:
            return Response({"status": False, "message": "Please enter contact number!"}, status=codes.CLIENT_ERROR)

    def patch(self, request):
        try:
            if request.user.is_authenticated:
                profile = BaseProfileModel.objects.get(user=request.user)
                serializer = BaseProfileSerializer(profile, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": f"Your profile has been updated!"}, status=codes.OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

class ProfilePictureAPI(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            picture = request.FILES.get('profile_picture')
            print(type(picture))
            print(request.FILES.get('profile_picture'))
            try:
                old_profile_picture = ProfilePicturesModel.objects.get(user=request.user)                
                serializer = ProfilePictureSerializer(old_profile_picture, data={'profile_picture': picture}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Profile picture updated!"}, status=codes.OK)
                else:
                    return Response({"status": False, "message": serializer.errors}, status=codes.SERVER_ERROR)        
            except ObjectDoesNotExist:
                serializer = ProfilePictureSerializer(data={'user': request.user.id, 'profile_picture': picture}) 
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Profile picture updated!"}, status=codes.OK)
                else:
                    return Response({"status": False, "message": serializer.errors}, status=codes.SERVER_ERROR)        
            except Exception as e:
                # from traceback import format_exc
                # print(format_exc(e))
                return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
        else:
            return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)

class ProviderProfileAPI(APIView):
    def get(self, request, pk=None):
        try:
            if pk is not None:
                provider_profile = ProviderProfileModel.objects.get(user__id=pk)
            else:
                provider_profile = ProviderProfileModel.objects.get(user__id=request.user.id)
            provider_profile_serializer = ProviderProfileSerializer(provider_profile)
            return Response({"status": True, "provider_profile": provider_profile_serializer.data}, status=codes.OK)    
        except ProviderProfileModel.DoesNotExist:
            return Response({"status": False, "message": "Requested record does not exist"}, status=codes.OK)
            
    def post(self, request):
        user = request.user
        if user.is_authenticated and user.is_active:
            if ProviderProfileModel.objects.filter(user=user).exists():
              return Response({"status": False, "message": "Profile already exists!"}, status=codes.SERVER_ERROR)
            else:
                serializer = ProviderProfileSerializer(data={**request.data, "user":user.id})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Your profile has been created!"}, status=codes.OK)
                else:
                    return Response({"status": False, "message": str(serializer._errors)}, status=codes.CLIENT_ERROR)
        else:
            return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        
    def patch(self, request):
        if request.user.is_authenticated and request.user.is_active:
            try:
                profile = ProviderProfileModel.objects.get(user=request.user)
                serializer = ProviderProfileSerializer(profile, data={**request.data, "user": request.user.id}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True}, status=codes.OK)
                else:
                    return Response({'status': False, 'message': serializer.errors}, status=codes.SERVER_ERROR)
            except ProviderProfileModel.DoesNotExist:
                return Response({'status': False, 'message': "Requested profile does not exist!"}, status=codes.CLIENT_ERROR)
            except Exception as e:
                return Response({'status': False, 'message': str(e)}, status=codes.SERVER_ERROR)
            
class EducationAPI(APIView):
    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    education = EducationModel.objects.get(user__id=pk)
                    serializer = EducationSerializer(education, many=True)
                    return Response({"status":True, "education_details": serializer.data}, status=codes.OK)
                else:
                    recordId = request.query_params.get('recordId')
                    if recordId is not None:
                        record = EducationModel.objects.get(id=recordId)
                        if record:
                            if request.user == record.user:                        
                                serializer = EducationSerializer(record)
                                return Response({"status":True, "record": serializer.data}, status=codes.OK)
                    else:
                        education = EducationModel.objects.filter(user=request.user)
                        serializer = EducationSerializer(education, many=True)
                        return Response({"status":True, "education_details": serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message": "Unauthorized!"}, status=codes.AUTH_ERROR)
        except Exception as e:
            print(e)
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
    
    def post(self, request):
        try:
            if request.user.is_authenticated and request.user.is_active:
                print(request.data)
                serializer = EducationSerializer(data={**request.data, "user": request.user.id})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Education details added"}, status=codes.OK)
                else:
                    print(serializer.errors)
                    return Response({"status":False, "message": serializer.errors}, status=codes.SERVER_ERROR)
            else:
                return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
    
    def patch(self, request, pk):
        try:
            
            id = pk 

            if request.user.is_authenticated and request.user.is_active:

                educational = EducationModel.objects.get(pk=id)

                serializer = EducationSerializer(educational, data=request.data, partial=True)

                if educational.user == request.user:
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status":True, "message":"Educational updated"}, status=codes.OK)
                    else:
                        print(serializer.errors)
                        return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
                else:
                    return Response({"status":False, "message":"login user not match"}, status=codes.AUTH_ERROR
                    )
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

    def delete(self,request, pk):
        try:
            if request.user.is_authenticated and request.user.is_active:
                education_record=EducationModel.objects.get(id=pk)
                if education_record.user == request.user:
                    education_record.delete()
                    return Response({'status':True, 'message': 'Education data removed!'},status=codes.OK)
                else:
                    return Response({"status":False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
    
class WorkExperienceAPI(APIView):
    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    experience = ExperienceModel.objects.filter(user__id=pk)
                    serializer = ExperienceSerializer(experience, many=True)
                    return Response({"status":True, "work_experiences": serializer.data}, status=codes.OK)
                else:
                    recordId = request.query_params.get('recordId')
                    if recordId is not None:
                        record = ExperienceModel.objects.get(id=recordId)
                        if record:
                            if request.user == record.user:
                                serializer = ExperienceSerializer(record)
                                return Response({"status":True, "record": serializer.data}, status=codes.OK)
                    else:
                        experience = ExperienceModel.objects.filter(user__id=request.user.id)
                        serializer = ExperienceSerializer(experience, many=True)
                        return Response({"status":True, "work_experiences": serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
    
    def post(self, request):
        try:
            if request.user.is_authenticated and request.user.is_active:
                serializer = ExperienceSerializer(data={**request.data, "user": request.user.id})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Work Experience added!"}, status=codes.OK)
                else:
                    print(serializer.errors)
                    return Response({"status":False, "message":serializer.errors}, status=codes.SERVER_ERROR)
            else:
                return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)
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
    
class ReportAPI(APIView):
    def get(self, request, pk=None, format=None):

        # it will view report as per the filter if filter is for payment then it will show data as per payment report or filter is for profile then profile report will be shown

        try:

            user = request.user
            if user.is_authenticated and user.is_active:
                report_type_id = request.query_params.get('report_type_filter')
                role_report_id = request.query_params.get('role_report_filter')

                if report_type_id is not None:
                    report_type_filter = ReportModel.objects.filter(report_type=report_type_id)
                    if report_type_filter:
                        serializer = ReportSerializer(report_type_filter, many=True)
                        return Response({"status":True, "message":"Reports displayed as per report types", "data":serializer.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status":False, "message":"Reports is not displayed as per report types"}, status=codes.CLIENT_ERROR)
                    
                if role_report_id is not None:
                    role_report_filter = ReportModel.objects.filter(role=role_report_id)
                    if role_report_filter:
                        serializer = ReportSerializer(role_report_filter, many=True)
                        return Response({"status":True, "message":"Reports displayed as per roles", "data":serializer.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status":False, "message":"Reports is not displayed as per role"}, status=codes.CLIENT_ERROR)
            
                else:

                    # it will give all type of data for example payment, profile, recruitment, job post report

                    report = ReportModel.objects.all()
                    serializer = ReportSerializer(report, many=True)
                    return Response({"status":True, "message":"All report is displayed", "data":serializer.data}, status=status.HTTP_200_OK)
                    
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def post(self, request, format=None):


        try:

            # it will post the report if report data is properly fill

            user = request.user
            if user.is_authenticated and user.is_active:
                user_role = user.role
                serializer = ReportSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(role=user_role)
                    return Response({"status":True, "message":"Report added sucesfully"}, status=status.HTTP_200_OK)
                else:

                    # if data is not fill proper then it will give message that report is not added

                    return Response({"status":False, "message":"Report not added"}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)
        
    def delete(self, request, pk, format=None):


        try:

            # it will check if given data is post by given user if it will match then user can delete that report data


            user = request.user
            if user.is_authenticated and user.is_active:
                id =pk 
                report = ReportModel.objects.get(pk=id)
                report.delete()
                return Response({"status":True, "message":"Report deleted sucesfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status":False, "message":"Token is not set properly"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)