from rest_framework.decorators import api_view
from .utils import *
from .models import Users
import datetime
from .managers.user_manager import UserManager

user_manager_obj = UserManager()


@api_view(['POST'])
@exception_handler
def login(request):
    headers, payload = request.META, request.data
    authorization = headers.get('HTTP_AUTHORIZATION')
    email, password = payload.get('email_id') or '', payload.get('password') or ''
    auth_token = UserManager.get_auth_token(email, password, authorization)
    return {"Authorization": auth_token, "data": "Logged-in"}


@api_view(['POST'])
@exception_handler
def sign_up(request):
    payload = request.data.dict()
    user_manager_obj.validate_signup_payload(payload)
    user_fields = filter_user_fields(payload)
    user_fields['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auth_token = generate_jwt(user_fields)
    user_fields['auth_token'] = auth_token
    user_obj = Users(**user_fields)
    user_obj.save()
    return {"Authorization": auth_token, "data": "Welcome User"}
