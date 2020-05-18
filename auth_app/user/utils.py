from rest_framework.response import Response
from rest_framework import status
from .exceptions import CustomException
from .serializers import UserSerializer
import jwt
import json
import base64
import time
import datetime
from .models import Users

with open('./config.json') as d:
    config = json.load(d)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return Response({"is_success": True, "data": data.get('data')},
                            headers={"Authorization": "Bearer " + data.get('Authorization')})
        except CustomException.ValidationError as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])}, status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        except CustomException.ForbiddenException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])}, status=status.HTTP_403_FORBIDDEN,
                            content_type="application/json")
        except CustomException.UnAuthorizeException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])}, status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        except CustomException.UserNotVerified as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])}, status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        except CustomException.InvalidException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])}, status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        except Exception as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
    return wrapper


def filter_user_fields(payload):
    return {key: value for key, value in payload.items() if key in UserSerializer.Meta.fields}


def get_error_dict(error):
    if isinstance(error, str):
        return error
    if isinstance(error, dict):
        return error
    error_message = {}
    error_dict = error.error_dict
    for key, val in error_dict.items():
        error_message[key] = val[0]
    return error_message


def generate_jwt(data):
    payload = data.copy()
    payload['iat'] = get_current_epoch()
    now = datetime.datetime.now() + datetime.timedelta(minutes=config['JWT_EXPIRY_MINUTES'])
    payload['expires'] = int(time.mktime(now.timetuple()))
    payload.pop('password')
    return jwt.encode(payload, config['SECRET_KEY'], algorithm="HS256").decode('utf-8')


def hash_pass(data):
    return base64.b64encode(str(data).encode("utf-8")).decode('utf-8')


def get_current_epoch():
    return int(time.time())

