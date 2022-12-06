from pyexpat import model
from pkg_resources import require
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import UserPicture

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPicture
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    profile_picture = ProfilePictureSerializer(required=False)

    class Meta:
        model = User
        fields =['id', 'email', 'username', 'password', 'profile_picture']
