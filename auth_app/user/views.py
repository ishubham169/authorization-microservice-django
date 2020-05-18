from rest_framework.decorators import api_view
from .utils import *
from .models import Users
from .exceptions import CustomException
import datetime
from .managers.user_manager import UserManager

user_manager_obj = UserManager()


@api_view(['POST'])
@exception_handler
def login(request):
    headers = request.header
    authorization = headers.get("Authorization")
    if not authorization:
        raise CustomException.UnAuthorizeException()


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
    return {"Authorization": auth_token, "data": "Signed-In"}
