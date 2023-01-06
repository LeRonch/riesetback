from dataclasses import field, fields
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Comment, Creation, Tag, UserPicture
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPicture
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile_picture = ProfilePictureSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'date_joined', 'profile_picture']


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            **attrs,
        }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    profile_picture = ProfilePictureSerializer(required=False)

    class Meta:
        model = User
        fields =['id', 'email', 'username', 'password', 'profile_picture']

class CurrentUserSerializer(serializers.ModelSerializer):
    """to JSON"""

    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    profile_picture = ProfilePictureSerializer(required=False)

    class Meta:
        model = User
        fields =['id', 'email', 'username', 'profile_picture']

class CreationFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creation
        fields= ['favorite']

class UserCreationSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = Creation
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UploadCreationSerializer(serializers.ModelSerializer):
    """to JSON"""

    title = serializers.CharField(required=True)
    creation = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    type = serializers.CharField(required=True)
    date = serializers.DateTimeField(required=False)
    tags = TagsSerializer(read_only=True, many=True)
    tags_list = serializers.ListField(required=True)
    fav = CreationFavSerializer(read_only=True, many=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Creation
        fields = '__all__'

class IncreaseDownloadCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creation
        fields = ['download_count']

class CommentSerializer(serializers.ModelSerializer):
    commenting_user = UserInfoSerializer()

    class Meta:
        model = Comment
        fields = '__all__'