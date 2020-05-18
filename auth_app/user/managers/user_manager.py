from ..exceptions import CustomException
from ..models import Users
from ..serializers import UserSerializer
from ..utils import *


class UserManager:

    @staticmethod
    def validate_signup_payload(payload):
        email = payload['email_id']
        is_user_exist = Users.objects.filter(email_id=email)
        if is_user_exist:
            raise CustomException.ValidationError("User already exist with this email")
        validation_error = {}
        for item in UserSerializer.Meta.fields:
            if item not in payload:
                if item in validation_error:
                    validation_error[item].append("{} is required field.".format(item))
                else:
                    validation_error[item] = ["{} is required field.".format(item)]

        password, conf_password = payload.get('password'), payload.get('confirm_password')
        for key, value in payload.items():
            if not value:
                raise CustomException.ValidationError("{} cannot be empty".format(key))
        if password and password != conf_password:
            validation_error['password'] = ["Both password not matching"]
        if validation_error:
            raise CustomException.ValidationError(validation_error)
        payload['password'] = hash_pass(password)
