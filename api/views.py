# *coding: utf-8*
from datetime import datetime
from api.serializers import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
import re

def customPagination(page_size):
    return type("SubClass", (PageNumberPagination,), {"page_size": page_size})

class UserListView(generics.ListAPIView):
    """
    get: Search or get users
    """
    permission_classes = (permissions.AllowAny, )

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'username')

class UserView(views.APIView):
    """
    get: receive user id, return user
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        id= self.kwargs['id']
        data = User.objects.get(id=id)
        return Response(UserSerializer(instance=data).data)

class RegisterView(views.APIView):
    """
    Post: register user
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        data = []

        try:
            upload = request.FILES['profile_picture']
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            user = User.objects.create(
                email=email,
                username=username,
            )
            user.set_password(password)
            user.save()
            user_picture = UserPicture.objects.create(
                user=user,
                profile_picture=upload
            )
            user_picture.save()
        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class UploadCreationView(views.APIView):
    """
    Post: add creation
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        serializer = UploadCreationSerializer(data=request.data)
        data = []

        try:
            upload = request.FILES['creation']
            serializer.is_valid(raise_exception=True)
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            type = serializer.validated_data['type']
            user_id = serializer.validated_data['user_id']
            tags_list = serializer.validated_data['tags_list']
            user = User.objects.get(id = user_id)
            date = datetime.now()

            creation = Creation.objects.create(
                creation=upload,
                title=title,
                description=description,
                date=date,
                download_count=0,
                fav_count=0,
                type=type,
                user=user,
            )
            creation.save()
            for tags_id_string in tags_list:
                tags_id_list = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', tags_id_string)
                for tag_id in tags_id_list:
                    tag = Tag.objects.get(id=tag_id)
                    tag.count += 1
                    tag.save()
                    creation.tags.add(tag)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class TagsView(generics.ListAPIView):

    """
    get: get tags
    """
    permission_classes = (permissions.AllowAny, )
    pagination_class = customPagination(page_size=50)
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer

class TagByIdView(generics.ListAPIView):

    """
    get: get tag by id
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        id= self.kwargs['id']
        data = Tag.objects.get(id=id)
        return Response(TagsSerializer(instance=data).data)

class CreationByUserView(views.APIView):

    """
    get: user creations
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Creation.objects.filter(user_id=id)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationByIdView(views.APIView):
    """
    get: creation by id
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Creation.objects.filter(id=id)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationByTagId(views.APIView):
    """
    get: creation by tag id
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Creation.objects.filter(tags=id)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationByName(views.APIView):
    """
    get: creation by name
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        name = self.kwargs['name']
        queryset = Creation.objects.filter(title__icontains=name)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)