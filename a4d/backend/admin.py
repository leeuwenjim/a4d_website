from django.contrib import admin
from .models import News, ThanxToModel, Page, Album, Photo, Sponsor, RouteImage, Route

# Register your models here.
admin.site.register(News)
admin.site.register(Page)
admin.site.register(ThanxToModel)
admin.site.register(Album)
admin.site.register(Sponsor)
admin.site.register(RouteImage)
admin.site.register(Route)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_year', 'image_day', 'image_name')
