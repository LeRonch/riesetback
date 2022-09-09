# *coding: utf-8*
from api.serializers import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class UserListView(generics.ListAPIView):
    """
    get: Search or get users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'username')
 