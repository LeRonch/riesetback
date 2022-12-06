from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView

router = DefaultRouter()

from api.views import *
urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls))
]