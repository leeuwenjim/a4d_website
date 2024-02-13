from django.contrib import admin
from .models import News, ThanxToModel, Page, Album, Photo

# Register your models here.
admin.site.register(News)
admin.site.register(Page)
admin.site.register(ThanxToModel)
admin.site.register(Album)
admin.site.register(Photo)
