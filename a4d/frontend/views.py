from django.http import Http404, JsonResponse
from django.shortcuts import render, reverse
from rest_framework.request import Request
from django.conf import settings
from backend.models import ThanxToModel, Page, News, Album, Photo
from a4d.utils import pages_slug_titles
from a4d.render import render_page_content
from backend.serializers import NewsSerializer
from backend.pagination import ApiRestPagination
import os
from django.http import HttpResponse


def get_menu():
    return [
        ['Nieuws', reverse('a4d_nieuws')],
        ['Informatie', '#', [
            ['Inschrijven', reverse('a4d_page', args=['inschrijven', ])],
            ['Startbureau &amp; controles', reverse('a4d_page', args=['controles', ])],
            ['Routes', reverse('a4d_page', args=['routes', ])],
            ['Parkeren', reverse('a4d_page', args=['parkeren', ])],
            ['Veelgestelde vragen', reverse('a4d_page', args=['faq', ])],
        ]],
        ['Foto&rsquo;s', reverse('a4d_gallery')],
        ['Over ons', '#', [
            ['A4D Hoevelaken', reverse('a4d_page', args=['over', ])],
            ['Verkeersregelaars', reverse('a4d_page', args=['verkeersregelaars', ])],
            ['Dank aan', reverse('a4d_page', args=['dank', ])],
            ['SGWB', reverse('a4d_page', args=['sgwb', ])],
        ]],
    ]  # 'over', 'verkeersregelaars', 'dank', 'sgwb', 'inschrijven', 'controles', 'routes', 'parkeren']


def favicon(request):
    static_dir = os.path.join(settings.BASE_DIR, 'statics/')
    with open(static_dir + 'img/favico.png', "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


def homepage(request):
    context = {
        'menu': get_menu(),
        'thanx': [thanx.name for thanx in ThanxToModel.objects.all().order_by('name')],
        'latest': NewsSerializer(News.objects.all().order_by('-publish_date', '-id')[:3], many=True).data
    }
    return render(request, 'a4d/home.html', context=context)


def page_view(request, page: str):
    if page not in pages_slug_titles.keys():
        print(page)
        print(pages_slug_titles.keys())
        raise Http404('Invalid page')

    page_obj = Page.get_page_from_slug(page)
    rendered_page = render_page_content(page_obj.content)

    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()],
        'content': rendered_page
    }

    return render(request, 'a4d/page.html', context)


def nieuws(request):
    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()]
    }

    return render(request, 'a4d/news.html', context)


def nieuws_api(request):
    return JsonResponse(
        ApiRestPagination(
            page_size=5
        ).paginate_raw_json(
            query_set=News.objects.all().order_by('-publish_date', '-id'),
            request=Request(request),
            serializer=NewsSerializer
        )
    )


def gallery(request, year=None, day=None):
    images = []
    years_menu = []
    menu = get_menu()
    thanx = [o.name for o in ThanxToModel.objects.all()]

    context = {
        'menu': menu,
        'thanx': thanx,
        'images': images,
        'year_menu': years_menu,
    }

    if Album.objects.all().count() == 0:
        return render(request, 'a4d/gallery.html', context)

    if year is None:
        latest_year = Album.objects.order_by('-year').values_list('year').first()
        if latest_year is not None:
            year = latest_year[0]

    years_queryset = Album.objects.order_by('-year').values_list('year').distinct()
    for query_year in years_queryset:
        albums = []
        if query_year[0] == year:
            for album in Album.objects.filter(year=year).order_by('title'):
                albums.append([
                    reverse('a4d_gallery_day', kwargs={'year': year, 'day': album.slug}),
                    album.title
                ])
        years_menu.append([
            reverse('a4d_gallery_year', kwargs={'year': query_year[0]}),
            str(query_year[0]),
            albums
        ])

    context['years_menu'] = years_menu

    if day is None:
        current_album = Album.objects.filter(year=year).order_by('title').first()
        if current_album is None:
            raise Http404('No album found')
    else:
        current_album = Album.objects.filter(slug=day).order_by('title').first()
        if current_album is None:
            raise Http404('No album found')

    for photo in current_album.photos.all():
        images.append(photo.image.url)

    context['title'] = current_album.title
    context['images'] = images


    return render(request, 'a4d/gallery.html', context)
