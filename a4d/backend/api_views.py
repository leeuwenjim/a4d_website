from time import sleep

from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from backend.utils import DetailApiView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import News, ThanxToModel, Page, Album, Photo
from .pagination import ApiRestPagination
from .serializers import ThanxToSerializer, UserSerializer, NewsSerializer, AlbumSerializer, ImageSerializer
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.contrib.auth.models import User
from a4d.utils import pages_slug_titles


class NewsOverview(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ApiRestPagination(
            page_size=5
        ).paginate(
            query_set=News.objects.all().order_by('-publish_date', '-id'),
            request=request,
            serializer=NewsSerializer
        )

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetails(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = News
    id_name = 'news_id'
    keyword = 'news'

    def get(self, request, news):
        return Response(NewsSerializer(news).data, status=status.HTTP_200_OK)

    def put(self, request, news):
        serializer = NewsSerializer(instance=news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news):
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThanxTo(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ThanxToModel.objects.all().order_by('name')

        return Response(ThanxToSerializer(data, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ThanxToSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThanxToDetails(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = ThanxToModel
    id_name = 't_id'
    keyword = 'thanx'

    def get(self, request, thanx: ThanxToModel):
        return Response(ThanxToSerializer(instance=thanx).data, status=status.HTTP_200_OK)

    def put(self, request, thanx: ThanxToModel):
        validator = ThanxToSerializer(instance=thanx, data=request.data)
        if validator.is_valid():
            validator.save()
            return Response(validator.data, status=status.HTTP_202_ACCEPTED)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, thanx: ThanxToModel):
        thanx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).order_by('full_name')
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ww1 = request.data['ww1']
        ww2 = request.data['ww2']

        new_user_serializer = UserSerializer(data=request.data)
        if new_user_serializer.is_valid() and ww1 == ww2:
            new_user = new_user_serializer.save()

            new_user.set_password(ww1)
            new_user.is_superuser = True
            new_user.is_staff = True
            new_user.save()

            return Response(new_user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(new_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = User
    id_name = 'user_id'
    keyword = 'user'

    def put(self, request, user):

        if 'ww1' in request.data and 'ww2' in request.data:
            ww1 = request.data['ww1']
            ww2 = request.data['ww2']

            if ww1 == ww2:
                user.set_password(ww1)
                user.save()

                if request.user.id == user.id:
                    update_session_auth_hash(request, user)

                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

            return Response({'password': 'Given passwords are not matching'}, status=status.HTTP_400_BAD_REQUEST)
        elif 'first_name' in request.data and 'last_name' in request.data and 'username' in request.data:
            serializer = UserSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if request.user.id == user.id: update_session_auth_hash(request, user)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Invalid data given'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user):
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PageEditView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):

        if slug not in pages_slug_titles.keys():
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = Page.get_page_from_slug(slug)

        return Response({'blocks': page.content}, status=status.HTTP_200_OK)

    def post(self, request, slug):
        if slug not in pages_slug_titles.keys():
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = Page.get_page_from_slug(slug)
        page.content = request.data['data']
        page.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumOverview(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        albums = Album.objects.all().order_by('-year')

        result_data = dict()

        for album in albums:
            if album.year not in result_data.keys():
                result_data[album.year] = list()
            result_data[album.year].append(AlbumSerializer(album).data)

        return Response({'data': result_data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetail(DetailApiView):
    permission_classes = [IsAuthenticated]

    model = Album
    id_name = 'album_id'
    keyword = 'album'

    def get(self, request, album):
        return Response(AlbumSerializer(album).data, status=status.HTTP_200_OK)

    def put(self, request, album):
        serializer = AlbumSerializer(instance=album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album):
        for photo in Photo.objects.filter(album=album):
            photo.image.delete()
            photo.delete()

        try:
            album.delete()
        except Exception:
            return Response({'error': 'Kon album niet verwijderen'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageOverview(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = Album
    keyword = 'album'
    id_name = 'album_id'

    def get(self, request, album: Album):
        return Response({'photos': [ImageSerializer(photo).data for photo in album.photos.all()]}, status=status.HTTP_200_OK)

    def post(self, request, album: Album):
        photo = Photo(album=album)
        photo.image = request.data['photo']
        try:
            photo.save()
            return Response(ImageSerializer(photo).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            pass
        return Response({'error': 'Could not save the image'}, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, album_id, photo_id):
        photo = Photo.objects.filter(id=photo_id).first();
        if photo and photo.album.id == album_id:
            return Response(ImageSerializer(photo).data, status=status.HTTP_200_OK)
        return Response({'error': 'photo not found or given photo is not a part of the given album'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, album_id, photo_id):
        photo = Photo.objects.filter(id=photo_id).first();
        if photo and photo.album.id == album_id:
            photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'photo not found or given photo is not a part of the given album'}, status=status.HTTP_404_NOT_FOUND)
