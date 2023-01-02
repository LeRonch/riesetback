from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, TagsView, UploadCreationView, CreationByUserView, CreationByIdView, TagByIdView

router = DefaultRouter()

from api.views import *
urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/<int:id>/', UserView.as_view(), name='user'),
    # path('user_profile/<int:id>/', name='user_profile'),
    # path('comments/<int:id>/', name='comments'),
    # path('creations', name='creations'),
    path('creation/<int:id>/',CreationByIdView.as_view(), name='creation'),
    path('tags/',TagsView.as_view(), name='tags'),
    path('tag/<int:id>',TagByIdView.as_view(), name='tag'),
    path('register/', RegisterView.as_view(), name='register'),
    path('upload/', UploadCreationView.as_view(), name='upload'),
    path('usercreations/<int:id>', CreationByUserView.as_view(), name='usercreations'),
    path('', include(router.urls)),
]