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
                                send_template_mail(subject=subject, to=email, context=  {'message': message, 'firstname': created_user.first_name}, template='confirmation_link')
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
                return Response({'status':False,'message':'Please provide email'}, status=codes.CLIENT_ERROR)


            if password is None:
                return Response({"status":False, "message":"Please provide password"}, status=codes.CLIENT_ERROR)
            

            # it will check in databse if email and password is wrong then it will give message that invalid email or password

            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active:
                    if user.check_password(password):
                        
                        # If password matches for the user, start a session for the user by logging them in
                        login(request, user)
                        
                        # After starting the session, get user's authentication token or create one if it is not yet generated
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response({"status":True, "token": token.key, "userData": {"first_name": user.first_name, "last_name": user.last_name}, 'message': 'Logged in succesfully!'}, status=codes.OK)    
                    else:
                        return Response({'status':False,'message': 'Invalid password!'},status=codes.CLIENT_ERROR)
                else:
                    return Response({'status':False,'message': 'Account is disabled'}, status=codes.CLIENT_ERROR)

            # if user is not active then it will display message that account is disabled
            except CustomUser.DoesNotExist:
                return Response({'status':False,'message':'Please provide correct email'},status=codes.CLIENT_ERROR)
            except ValidationError as valError:
                # print(valError)
                return Response({'status':False,'message': str(valError)},status=codes.CLIENT_ERROR)
            except Exception as e:
                return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)


class UserProfileView(APIView):

    def get(self, request, pk=None):
        try:
            if request.user.is_authenticated:
                if pk is not None:
                    base_profile = BaseProfileModel.objects.get(user__id=pk)
                else:
                    base_profile = BaseProfileModel.objects.get(user__id=request.user.id)
                base_profile_serializer = BaseProfileSerializer(base_profile)
                return Response({"status":True, "base_profile":base_profile_serializer.data}, status=codes.OK)
            else:
                return Response({"status":False, "message":"User is not authenticated"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.CLIENT_ERROR)

    def post(self, request):
        try:
            user = request.user
            required_fields = {'city', 'address', 'zipcode','phone_number','whatsapp_number', 'about_us','language_info','instagram_info','facebook_info'}
            if user.is_authenticated and user.is_active:
                for field in required_fields:
                    if field not in request.data:
                        return Response({"status": False, "message": "all fields must be required"}, status=codes.CLIENT_ERROR)
                    
                mutable_data = request.data.copy()
                mutable_data['user'] = user.id 

                serializer = BaseProfileSerializer(data=mutable_data)
                if serializer.is_valid():
                    email = user.email
                    if BaseProfileModel.objects.filter(user__email=email).exists():
                        return Response({"status": False, "message": "user profile already exists"}, status=codes.CONFLICT)
                    serializer.save()  # Pass the user object instead of the user ID
                    return Response({"status": True, "message": "User profile added"}, status=codes.OK)
                else:
                    # Return error message for serializer errors
                    error_message = "Invalid data provided. Please check the following errors:"
                    errors = []
                    for field, field_errors in serializer.errors.items():
                        field_errors = [str(error) for error in field_errors]
                        errors.append(f"{field}: {', '.join(field_errors)}")
                    return Response({"status": False, "message": {"error_message": error_message, "errors": errors}}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)
        
        
    def patch(self, request):
        try:
            user = request.user
            allowed_fields = {'user_name', 'profile_pic', 'city', 'address', 'zipcode', 'phone_number', 'whatsapp_number','about_us', 'language_info','instagram_info', 'facebook_info'}
            if user.is_authenticated and user.is_active:
                updated_field = None
                for field in allowed_fields:
                    if field in request.data:
                        updated_field = field
                        break
                if not updated_field:
                    return Response({"status": False, "message": "No valid field to update"}, status=codes.CLIENT_ERROR)
                email = user.email
                profile = BaseProfileModel.objects.filter(user__email=email).first()

                profile_pic = ProfilePicModel.objects.get(user=user)

                serializer = BaseProfileSerializer(profile, data={updated_field: request.data[updated_field]}, partial=True)

                profile_pic_serializer = ProfilePicSerializer(profile_pic, data={updated_field: request.data[updated_field]}, partial=True)

                if 'profile_pic' in request.data:
                    if profile_pic_serializer.is_valid():

                        print("--------- PROFILE PIC : ",type(request.data.get("profile_pic")))
                        
                        profile_pic_serializer.save()
                        return Response({"status":True, "message":"Profile pic updated"}, status=codes.OK)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": f"User profile field '{updated_field}' updated"}, status=codes.OK)
                else:
                    # Return error message for serializer errors
                    error_message = "Invalid data provided. Please check the following errors:"
                    errors = []
                    for field, field_errors in serializer.errors.items():
                        field_errors = [str(error) for error in field_errors]
                        errors.append(f"{field}: {', '.join(field_errors)}")
                    return Response({"status": False, "message": {"error_message": error_message, "errors": errors}}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if user.is_authenticated and user.is_active:
                id = pk
                base_model = BaseProfileModel.objects.get(pk=id)
                base_model.delete()
                return Response({"status":True, "message":"Base profile data is deleted"}, status=codes.OK)
            else:
                return Response({"status": False, "message": "Authentication token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status":False, "message":str(e)}, status=codes.SERVER_ERROR)

class UserRatingView(APIView):
    def post(self, request):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                serializer = UserRatingSerializer(data={**request.data, "rated_by": request.user.id})
                rated_user = request.data["rated_user"]

                if user.id == rated_user:
                    return Response({"status": False, "message": "Same user cannot provide a rating to themselves"}, status=codes.CONFLICT)
                
                is_exist = RatingModel.objects.filter(rated_by=request.user.id, rated_user=rated_user).exists()

                if is_exist:
                    return Response({"status": False, "message": "Same user cannot provide another rating"}, status=codes.CONFLICT)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": True, "message": "Rating given to user", "data": serializer.data}, status=codes.OK)
                else:
                    error_message = "Invalid data provided. Please check the following errors:"
                    errors = []
                    for field, field_errors in serializer.errors.items():
                        field_errors = [str(error) for error in field_errors]
                        errors.append(f"{field}: {', '.join(field_errors)}")
                    return Response({"status": False, "message": {"error_message": error_message, "errors": errors}}, status=codes.CLIENT_ERROR)
            else:
                return Response({"status": False, "message": "Token is not set properly"}, status=codes.AUTH_ERROR)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=codes.SERVER_ERROR)   

    def get(self, request):
        try:
            user = request.user
            if user.is_authenticated and user.is_active:
                ratings = RatingModel.objects.filter(rated_user=user)
                serializer = UserRatingSerializer(ratings, many=True)
                return Response(
                    {"status": True, "message": "Ratings for the user", "data": serializer.data},
                    status=codes.OK
                )
            else:
                return Response(
                    {"status": False, "message": "Token is not set properly"},
                    status=codes.AUTH_ERROR
                )
        except Exception as e:
            return Response(
            {"status": False, "message": str(e)},
            status=codes.SERVER_ERROR
        )