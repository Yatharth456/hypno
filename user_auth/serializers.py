from rest_framework import serializers
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email", "username", "password",)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email",)
