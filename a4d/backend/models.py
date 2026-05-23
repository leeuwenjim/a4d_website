from django.db import models
import re

from backend.slugify import unique_slugify


# THIS FUNCTION IS HERE FOR BACKWARD MIGRATIONS BUT UNUSED!!
def news_image_upload_location(instance, filename):
    return 'images/news/{}'.format(filename)


def picture_upload_location(instance: 'Photo', filename):
    return 'images/photos/{}/{}/{}'.format(instance.album.year, instance.album.title, filename)

def sponsor_logo_upload(instance: 'Sponsor', filename):
    return 'images/sponsor/logo/{}'.format(filename)

def sponsor_extra_image_upload(instance: 'Sponsor', filename):
    return 'images/sponsor/extra/{}'.format(filename)

def routes_image_upload(instance: 'RouteImage', filename):
    return 'images/routes/{}'.format(filename)

def routes_walking_image_upload(instance: 'RouteImage', filename):
    return 'images/walking_routes/{}'.format(filename)

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

    def __str__(self):
        name = self.image.name.split('/')
        return f"<Photo id: {self.id}>; image: /{name[-3]}/{name[-2]}/{name[-1]}>"
    
    def image_year(self):
        name = self.image.name.split('/')
        return name[-3]
    image_year.short_description = 'Year'
    
    def image_day(self):
        name = self.image.name.split('/')
        return name[-2]
    image_day.short_description = 'Day'

    def image_name(self):
        name = self.image.name.split('/')
        return name[-1]
    image_name.short_description = 'Name'

    def __repr__(self):
        return self.__str__()




class RouteImage(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to=routes_image_upload, max_length=255, null=False, blank=False)

    def __str__(self):
        return f"<RouteImage; {self.title}>"

    def __repr__(self):
        return self.__str__()
    

def route_helper_index_to_name(index: int) -> str:
    lookup = ['ERR','di5', 'wo5', 'do5', 'vr5', 'di10', 'wo10', 'do10', 'vr10']
    return lookup[index]


class Route(models.Model):
    # 1: di_5km, 2: wo_5km, 3: do_5km, 4: vr_5km
    # 5: di_10km, 6: wo_10km, 7: do_10km, 8: vr_10km

    ROUTE_CHOICES = [(i, f"Image {route_helper_index_to_name(i)}") for i in range(1, 9)]
    
    slot = models.PositiveSmallIntegerField(unique=True, choices=ROUTE_CHOICES)
    image = models.ImageField(upload_to=routes_walking_image_upload, max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"<Route: {route_helper_index_to_name(self.slot)}>"

    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def get_route(cls, index: int):
        if any(i == index for i, _ in cls.ROUTE_CHOICES):
            return Route.objects.get_or_create(slot = index)[0]
        return None



class Sponsor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=sponsor_logo_upload, null=True, blank=True, max_length=255)
    extra = models.ImageField(upload_to=sponsor_extra_image_upload, null=True, blank=True, max_length=255)

    def __str__(self):
        return f"<Sponsor: {self.name}>"
    
    def __repr__(self):
        return self.__str__()