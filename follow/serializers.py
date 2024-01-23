from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from follow.utils import send_verification_code
from .models import CustomUser
from django.db import models
from django.contrib.auth.forms import SetPasswordForm

class UserRegisterSerializers(ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ['username','email','password',]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class UserCodeSerializers(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['code', ]

class UserSendCodeSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email",]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['old_password','new_password','confirm_new_password',]