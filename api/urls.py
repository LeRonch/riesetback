from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, TagsView, UploadCreationView, CreationByUserView, CreationByIdView, TagByIdView, CreationByTagIdView, CreationByNameView, CreationLatestView, CreationFavView, LinksView, DowloadCountIncreaseView, PostFavoriteView, DeleteFavoriteView, FavCreationByIdView, DescriptionView

router = DefaultRouter()

from api.views import *
urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/<int:id>/', UserView.as_view(), name='user'),
    # path('user_profile/<int:id>/', name='user_profile'),
    # path('comments/<int:id>/', name='comments'),
    path('creationsfav/',CreationFavView.as_view(), name='creationsfav'),
    path('creationslatest/',CreationLatestView.as_view(), name='creationslatest'),
    path('creation/<int:id>/',CreationByIdView.as_view(), name='creation'),
    path('creationname/<str:name>/',CreationByNameView.as_view(), name='creationtag'),
    path('creationtag/<int:id>/',CreationByTagIdView.as_view(), name='creationtag'),
    path('favcreation/<int:id>/',FavCreationByIdView.as_view(), name='favcreation'),
    path('tags/',TagsView.as_view(), name='tags'),
    path('tag/<int:id>',TagByIdView.as_view(), name='tag'),
    path('dowloadcount/',DowloadCountIncreaseView.as_view(), name='dowloadcount'),
    path('postfavorite/', PostFavoriteView.as_view(), name='postfavorite'),
    path('deletefavorite/', DeleteFavoriteView.as_view(), name='deletefavorite'),
    path('register/', RegisterView.as_view(), name='register'),
    path('links/', LinksView.as_view(), name='register'),
    path('desc/', DescriptionView.as_view(), name='desc'),
    path('upload/', UploadCreationView.as_view(), name='upload'),
    path('usercreations/<int:id>', CreationByUserView.as_view(), name='usercreations'),
    path('', include(router.urls)),
]