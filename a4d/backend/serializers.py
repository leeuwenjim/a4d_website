from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ThanxToModel, News, Album, Photo, Sponsor


class ThanxToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanxToModel
        fields = ['id', 'name']
        read_only_fields = ['id', ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']
        read_only_fields = ['id', ]

class NewsSerializer(serializers.ModelSerializer):
    published_on = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_on', 'link']
        read_only_fields = ['id', 'published_on']

    def get_published_on(self, instance: News):
        print('-'*50)
        print(instance)
        print(instance.publish_date)
        print(type(instance.publish_date))
        print('-' * 50)
        return instance.publish_date.strftime('%d-%m-%Y')

class SponsorSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    extra_url = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'content', 'logo_url', 'extra_url']
        read_only_fields = ['id', 'logo_url', 'extra_url']
    
    def get_logo_url(self, instance: Sponsor):
        print(instance)
        if instance.logo:
            return instance.logo.url
        return ""
    
    def get_extra_url(self, instance: Sponsor):
        if (instance.extra):
            return instance.extra.url
        return ""

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'slug', 'year']
        read_only_fields = ['id', 'slug']
        extra_kwargs = {
            'year': {'write_only': True},
        }

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'url']
        read_only_fields = fields

    def get_url(self, instance: Photo):
        return instance.image.url
