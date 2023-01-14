# *coding: utf-8*
from datetime import datetime
from api.models import Comment
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
from django.db.models import F


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
                profile_picture=upload,
                twitter_link='null',
                patreon_link='null',
                paypal_link='null',
                description='null'
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

class CreationByTagIdView(views.APIView):
    """
    get: creation by tag id
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Creation.objects.filter(tags=id)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationByNameView(views.APIView):
    """
    get: creation by name
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        name = self.kwargs['name']
        queryset = Creation.objects.filter(title__icontains=name)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationFavView(views.APIView):
    """
    get: 5 top creation
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        queryset = Creation.objects.all().order_by('-fav_count')[:5]
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class CreationLatestView(views.APIView):
    """
    get: 5 last creation
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        queryset = Creation.objects.all().order_by('-date')[:5]
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class LinksView(views.APIView):
    """
    put: updte links
    """
    permission_classes = (permissions.AllowAny, )
    def put(self, request):

        serializer = ProfilePictureSerializer(data=request.data)
        data = []

        try:
            serializer.is_valid(raise_exception=True)
            user = request.data['user_id']
            twitter = serializer.validated_data['twitter_link']
            paypal = serializer.validated_data['paypal_link']
            patreon = serializer.validated_data['patreon_link']

            UserPicture.objects.filter(user=user).update(twitter_link=twitter, paypal_link=paypal, patreon_link=patreon)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class DowloadCountIncreaseView(views.APIView):
    """
    put: increase download count
    """
    permission_classes = (permissions.AllowAny, )
    def post(self, request):

        serializer = IncreaseDownloadCountSerializer(data=request.data)
        data = []

        try:
            serializer.is_valid(raise_exception=True)
            creation_id = request.data['creation_id']

            Creation.objects.filter(id=creation_id).update(download_count = F('download_count') + 1)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class PostFavoriteView(views.APIView):
    """
    post: add to favorite
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = []

        try:
            creation_id = request.data['creation_id']
            user_id = request.data['user_id']

            Creation.objects.filter(id=creation_id).update(fav_count = F('fav_count') + 1)
            creation = Creation.objects.get(id=creation_id)
            user = User.objects.get(id=user_id)
            creation.favorite.add(user)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class DeleteFavoriteView(views.APIView):
    """
    delete: delete favorite
    """
    permission_classes = (permissions.AllowAny, )

    def delete(self, request):

        data = []

        try:
            creation_id = request.data['creation_id']
            user_id = request.data['user_id']

            Creation.objects.filter(id=creation_id).update(fav_count = F('fav_count') - 1)
            creation = Creation.objects.get(id=creation_id)
            user = User.objects.get(id=user_id)
            creation.favorite.remove(user)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class DeleteCreationView(views.APIView):
    """
    delete: delete creation
    """
    permission_classes = (permissions.AllowAny, )

    def delete(self, request):

        data = []

        try:
            creation_id = request.data['creation_id']
            Creation.objects.get(id=creation_id).delete()

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class FavCreationByIdView(views.APIView):
    """
    get: fav creation by user id
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Creation.objects.filter(favorite=id)
        return Response(UserCreationSerializer(instance=queryset, many=True).data)

class DescriptionView(views.APIView):
    """
    put: user desc
    """
    permission_classes = (permissions.AllowAny, )

    def put(self, request):
        data = []
        try:
            user = request.data['user_id']
            description = request.data['description']

            UserPicture.objects.filter(user=user).update(description=description)

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)

class PostCommentView(views.APIView):
    """
    post: comment
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = []
        try:
            user_id = request.data['user_id']
            creation_id = request.data['creation_id']
            content = request.data['comment']
            date = datetime.now()

            user = User.objects.get(id = user_id)
            creation = Creation.objects.get(id = creation_id)

            comment = Comment.objects.create(
                content = content,
                commenting_user = user,
                creation = creation,
                date = date
            )

            comment.save()

        except ValidationError as err:
            data = {'success': False, 'message': str(err)}

        return Response(data)


class GetCommentsView(views.APIView):
    """
    get: comments for a creation
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        queryset = Comment.objects.filter(creation=id).order_by('-date')
        return Response(CommentSerializer(instance=queryset, many=True).data)