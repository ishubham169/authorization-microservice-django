from rest_framework.response import Response
from rest_framework import status
from .exceptions import CustomException
from .serializers import UserSerializer
import jwt
import json
import base64
import time
import datetime

with open('./config.json') as d:
    config = json.load(d)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            data, response, headers = result.get('data') or '', {"is_success": True}, {}
            if data:
                response.update({"data": data})
            auth_token = result.get('Authorization') or {}
            if auth_token:
                headers = {"Authorization": auth_token,
                           "Access-Control-Expose-Headers": "Authorization"}
            return Response(response, headers=headers)
        except CustomException.ValidationError as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        except CustomException.ForbiddenException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_403_FORBIDDEN,
                            content_type="application/json")
        except CustomException.UnAuthorizeException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        except CustomException.UserNotVerified as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        except CustomException.InvalidException as ae:
            return Response({"is_success": False, "data": {}, "error": get_error_dict(ae.args[0])},
                            status=status.HTTP_400_BAD_REQUEST,
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
    now = datetime.datetime.now() + datetime.timedelta(minutes=config['TOKEN_EXPIRY_MINUTES'])
    payload['expires'] = int(time.mktime(now.timetuple()))
    payload.pop('password')
    return jwt.encode(payload, config['SECRET_KEY'], algorithm="HS256").decode('utf-8')


def encode(data):
    return base64.b64encode(str(data).encode("utf-8")).decode('utf-8')


def decode(data):
    if '===' not in data:
        data = data + '==='
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")


def get_current_epoch():
    return int(time.time())


def is_token_expired(token):
    data = json.loads(decode(token))
    expires = data['expires']
    return False if get_current_epoch() - expires > 0 else True


def verify_jwt(token):
    try:
        jwt.decode(token, config['SECRET_KEY'], algorithms="HS256")
    except Exception:
        raise CustomException.UnAuthorizeException("UnAuthorised")
