# *coding: utf-8*
from api.serializers import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import views
from rest_framework.pagination import PageNumberPagination

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

class TagsView(generics.ListAPIView):

    """
    get: get tags
    """
    permission_classes = (permissions.AllowAny, )
    pagination_class = customPagination(page_size=50)
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
