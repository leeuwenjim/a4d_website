from time import sleep

from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from backend.utils import DetailApiView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import News, ThanxToModel, Page, Album, Photo, Sponsor, RouteImage, Route
from .pagination import ApiRestPagination
from .serializers import ThanxToSerializer, UserSerializer, NewsSerializer, AlbumSerializer, ImageSerializer, SponsorSerializer, RouteImageSerializer, RouteSerializer
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

class RouteBaseOverview(APIView):
    def get(self, request):
        return Response({"success": "false", "details": "Endpoint not impemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class RouteImageOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = RouteImage.objects.all().order_by('id')
        return Response(RouteImageSerializer(data, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RouteImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        routeimg = RouteImage(title=serializer.validated_data['title'])
        
        routeimg.image = request.data['image']
        try:
            routeimg.save()
            return Response(RouteImageSerializer(routeimg).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
        return Response({'image': ['Could not save the image', ]}, status=status.HTTP_400_BAD_REQUEST) 


class RouteImageDetailView(DetailApiView):
    permission_classes = [IsAuthenticated]

    model = RouteImage
    id_name = 'img_id'
    keyword = 'route_image'

    def get(self, request, route_image: RouteImage):
        return Response(RouteImageSerializer(route_image).data, status=status.HTTP_200_OK)
    
    def post(sef, request, route_image: RouteImage):
        route_image.image.delete()
        route_image.image = request.data['image']
        try:
            route_image.save()
            return Response(RouteImageSerializer(route_image).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
        return Response({'error': 'Could not save the image'}, status=status.HTTP_400_BAD_REQUEST) 
    
    def put(sef, request, route_image: RouteImage):
        serializer = RouteImageSerializer(instance=route_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, route_image:RouteImage):
        route_image.image.delete()
        route_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RouteOverview(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Route.objects.all().order_by('slot')
        return Response(RouteSerializer(data, many=True).data, status=status.HTTP_200_OK)

class RouteDetailview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, route_id: int):
        route: Route = Route.get_route(route_id)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(RouteSerializer(route).data, status=status.HTTP_200_OK)
    
    def post(self, request, route_id: int):
        route: Route = Route.get_route(route_id)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = RouteSerializer(instance=route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RouteAttachmentDetailView(APIView):
    def get(self, request, route_id: int):
        route: Route = Route.get_route(route_id)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        img_url = ''
        if (route.image):
            img_url = route.image.url
        return Response({'slot': route_id, 'image': img_url}, status=status.HTTP_200_OK)
    
    def post(self, request, route_id: int):
        route: Route = Route.get_route(route_id)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if (route.image):
            route.image.delete()
        route.image = request.data['image']
        try:
            route.save()
        except Exception as e:
            print(e)
            return Response({'image': ['Could not save the image', ]}, status=status.HTTP_400_BAD_REQUEST)
        
        img_url = route.image.url
        return Response({'slot': route_id, 'image': img_url}, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, route_id: int):
        route: Route = Route.get_route(route_id)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if (route.image):
            route.image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class SponsorOverview(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Sponsor.objects.all().order_by('name')

        return Response(SponsorSerializer(data, many=True).data, status=status.HTTP_200_OK)
        #data = Sponsor.objects.all().order_by("name")
        #return Response(SponsorSerializer(data, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SponsorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SponsorDetailview(DetailApiView):
    permission_classes = [IsAuthenticated]

    model = Sponsor
    id_name = 'sponsor_id'
    keyword = 'sponsor'

    def get(self, request, sponsor):
        return Response(SponsorSerializer(sponsor).data, status=status.HTTP_200_OK)
    
    def put(self, request, sponsor):
        serializer = SponsorSerializer(instance=sponsor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, sponsor):
        sponsor.logo.delete()
        sponsor.extra.delete()
        sponsor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SponsorLogoView(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = Sponsor
    keyword = 'sponsor'
    id_name = 'sponsor_id'

    def get(self, request, sponsor: Sponsor):
        data = SponsorSerializer(sponsor).data;
        return Response({'logo': data['logo_url']}, status=status.HTTP_200_OK)

    def post(self, request, sponsor: Sponsor):
        sponsor.logo.delete()
        sponsor.logo = request.data['logo']
        try:
            sponsor.save()
            return Response({'logo': SponsorSerializer(sponsor).data['logo_url']}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
        return Response({'error': 'Could not save the image'}, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, sponsor: Sponsor):
        sponsor.logo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SponsorExtraView(DetailApiView):

    permission_classes = [IsAuthenticated]

    model = Sponsor
    keyword = 'sponsor'
    id_name = 'sponsor_id'

    def get(self, request, sponsor: Sponsor):
        data = SponsorSerializer(sponsor).data;
        return Response({'extra': data['extra_url']}, status=status.HTTP_200_OK)

    def post(self, request, sponsor: Sponsor):
        sponsor.extra.delete()
        sponsor.extra = request.data['extra']
        try:
            sponsor.save()
            return Response({'extra': SponsorSerializer(sponsor).data['extra_url']}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
        return Response({'error': 'Could not save the image'}, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, sponsor: Sponsor):
        sponsor.extra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            print(e)
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
