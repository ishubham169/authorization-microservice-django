from ..utils import *
from ..exceptions import CustomException
from ..models import Users
from ..serializers import UserSerializer


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
        payload['password'] = encode(password)

    @staticmethod
    def get_auth_token(email, password, authorization):
        if not authorization:
            try:
                user = Users.objects.get(email_id=email, password=encode(password))
            except Exception:
                raise CustomException.UnAuthorizeException("Invalid email/password")
            auth_token = user.auth_token
            try:
                is_token_valid = is_token_expired(auth_token.split('.')[1])
            except Exception:
                raise CustomException.UnAuthorizeException("Not Authorized")
            if not is_token_valid:
                user_details = filter_user_fields(user.__dict__)
                updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_details['updated'] = updated_at
                new_auth_token = generate_jwt(user_details)
                user.auth_token = new_auth_token
                user.updated = updated_at
                user.save()
                return new_auth_token
            else:
                return auth_token
        else:
            try:
                auth_token = is_token_expired(authorization.split('.')[1])
            except Exception:
                raise CustomException.UnAuthorizeException("Not Authorized")
            if is_token_expired(auth_token):
                return auth_token
            else:
                raise CustomException.UnAuthorizeException("Not Authorized")
