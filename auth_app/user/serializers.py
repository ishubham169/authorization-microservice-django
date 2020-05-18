from .models import Users
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['name', 'email_id', 'phone_number', 'gender', 'password']