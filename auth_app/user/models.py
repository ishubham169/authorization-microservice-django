from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .exceptions import CustomException


class Users(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email_id = models.EmailField(max_length=50, blank=False, validators=[validate_email])
    phone_number = models.CharField(null=False, max_length=10, blank=False)
    gender = models.CharField(max_length=6)
    auth_token = models.CharField(max_length=500, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=2934)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            raise CustomException.ValidationError(e)
        super().save(*args, **kwargs)
