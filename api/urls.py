from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, TagsView

router = DefaultRouter()

from api.views import *
urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/<int:id>/', UserView.as_view(), name='user'),
    # path('user_profile/<int:id>/', name='user_profile'),
    # path('comments/<int:id>/', name='comments'),
    # path('creations', name='creations'),
    # path('creation/<int:id>/', name='creation'),
    path('tags/',TagsView.as_view(), name='tags'),
    # path('tags/<int:id>', name='tag'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls))
]