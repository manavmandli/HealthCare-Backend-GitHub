from rest_framework.views import APIView
from rest_framework.response import Response
from constants.status import codes
from .models import NotificationModel
from .serializers import NotificationSerializer

# Create your views here.

class NotificationsAPI(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated and request.user.is_active:
                notifications = NotificationModel.objects.filter(reciever=request.user)
                serializer = NotificationSerializer(notifications, many=True)
                return Response({"status": True, "notifications": serializer.data}, status=codes.OK)  
            else:
                return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)  
        except Exception as e:
            print("notifications get exception : ", e)
            return Response({"status": False, "message": "There was an error!"}, status=codes.SERVER_ERROR)  
            

    def patch(self, request):
        try:
            print(request.user)
            if request.user.is_authenticated and request.user.is_active:
                notifications = NotificationModel.objects.filter(reciever=request.user, is_read=False)
                notifications.update(is_read=True)
                return Response({"status": True}, status=codes.OK)
            else:
                return Response({"status": False, "message": "Unauthorized"}, status=codes.AUTH_ERROR)  
        except Exception as e:
            print("notifications read exception : ", e)
            return Response({"status": False, "message": "There was an error!"}, status=codes.SERVER_ERROR)  
            

class NotificationBeatAPI(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated and request.user.is_active:
                notifications = NotificationModel.objects.filter(reciever=request.user, is_read=False).count()
                if notifications > 0:
                    return Response({"status": True}, status=codes.OK)
                else:
                    return Response({"status": False}, status=codes.OK)
        except Exception:
            return Response({"status": False}, status=codes.OK)
                
                
        
            
            



