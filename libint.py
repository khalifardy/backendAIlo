from rest_framework.permissions import BasePermission
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import jwt

class KonversiChoice:
    
    def gender(self,no):
        konvert={
            "PRIA" : 1,
            "WANITA" : 2
        }

        return konvert[no]
    
    def religion(self,no):
        konvert={
            "ISLAM" : 1,
            "KRISTEN" : 2,
            "KATHOLIK" : 3,
            "HINDU" : 4,
            "BUDDHA" : 5,
            "OTHER_RELIGION" : 6
        }

        return konvert[no]
    
    def status(self,no):
        konvert={
            "ACTIVE" : 1,
            "TERMINATE" : 2,
            "RESIGN" : 3,
            "ALUMNI" : 4,
            "OTHER_STAFF_STATUS" : 5
        }

        return konvert[no]
    
    def levels(self,no):
        konvert = {
            "DIREKTUR" : 1,
            "WADIR" : 2,
            "KOORDAS" : 3,
            "KADIV" : 4,
            "STAFF" : 5
        }

        return konvert[no]
    
class IsTokenValid(BasePermission):

    def has_permission(self, request, view):
        try:
            try:
                token = request.auth.decode("utf-8")
            except Exception as e:
                token = request.META['HTTP_AUTHORIZATION']
                token = token.replace("Bearer ", "")

            if token is not None:
                is_allowed_user = True
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                payload = jwt_decode_handler(token)
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
                

            else:
                is_allowed_user = False
        except Exception as e:
            print ("verify_token_error :" + str(e))
            is_allowed_user = False
        return is_allowed_user