from django.db import models
import re

from backend.slugify import unique_slugify


# THIS FUNCTION IS HERE FOR BACKWARD MIGRATIONS BUT UNUSED!!
def news_image_upload_location(instance, filename):
    return 'images/news/{}'.format(filename)


def picture_upload_location(instance: 'Photo', filename):
    return 'images/photos/{}/{}/{}'.format(instance.album.year, instance.album.title, filename)

class News(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField()
    publish_date = models.DateField(null=False, blank=True, auto_now_add=True)
    link = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '<News: {}>'.format(self.title)

    def __repr__(self):
        return self.__str__()

class ThanxToModel(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Page(models.Model):
    slug = models.CharField(max_length=90, null=False, blank=False, unique=True)
    content = models.TextField(null=True, blank=True)

    @staticmethod
    def get_page_from_slug(slug):
        page, created = Page.objects.get_or_create(slug=slug, defaults={'content': '[]'})
        return page


    def __str__(self):
        return f'<Page: {self.slug}>'

    def __repr__(self):
        return self.__str__()


class Album(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=True)
    year = models.IntegerField()

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'<Album: {self.year} - {self.title}>'

    def __repr__(self):
        return self.__str__()


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=False, blank=False, related_name='photos')
    image = models.ImageField(upload_to=picture_upload_location, max_length=255, null=False, blank=False)
