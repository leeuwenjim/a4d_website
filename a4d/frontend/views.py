from django.http import Http404, JsonResponse
from django.shortcuts import render, reverse
from rest_framework.request import Request
from django.conf import settings
from backend.models import ThanxToModel, Page, News, Album, Photo, Sponsor, RouteImage, Route
from a4d.utils import pages_slug_titles
from a4d.render import render_page_content
from backend.serializers import NewsSerializer
from backend.pagination import ApiRestPagination
import os
from django.http import HttpResponse
from backend.utils import create_header_data, create_image_data, create_text_data


def get_menu():
    return [
        ['Nieuws', reverse('a4d_nieuws')],
        ['Informatie', '#', [
            ['Inschrijven', reverse('a4d_page', args=['inschrijven', ])],
            ['Startbureau &amp; controles', reverse('a4d_page', args=['controles', ])],
            ['Routes', reverse('a4d_routes')],
            ['Parkeren', reverse('a4d_page', args=['parkeren', ])],
            ['Veelgestelde vragen', reverse('a4d_page', args=['faq', ])],
        ], 'info'],
        ['Foto&rsquo;s', reverse('a4d_gallery')],
        ['Over ons', '#', [
            ['A4D Hoevelaken', reverse('a4d_page', args=['over', ])],
            ['Verkeersregelaars', reverse('a4d_page', args=['verkeersregelaars', ])],
            ['Dank aan', reverse('a4d_page', args=['dank', ])],
            ['SGWB', reverse('a4d_page', args=['sgwb', ])],
        ], 'about'],
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

    extra_page_data = None
    if (page == 'dank'):
        extra_page_data = list()
        for sponsor in Sponsor.objects.all().order_by('name'):
            extra_page_data.append(create_header_data(sponsor.name, 3))
            if sponsor.content:
                extra_page_data.append(create_text_data(sponsor.content.replace("\r\n", "<br />")))
            if (sponsor.logo):
                extra_page_data.append(create_image_data(sponsor.logo.url, style_class="sponsor-image"))
            if (sponsor.extra):
                extra_page_data.append(create_image_data(sponsor.extra.url, style_class="sponsor-image"))   

    rendered_page = render_page_content(page_obj.content, extra_page_data)

    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()],
        'content': rendered_page
    }

    return render(request, 'a4d/page.html', context)

def page_routes(request):
    page_obj = Page.get_page_from_slug('routes')
    rendered_page = render_page_content(page_obj.content, None)
    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()],
        'content': rendered_page
    }

    extra_content = list()
    for route_image in RouteImage.objects.all().order_by('id'):
        extra_content.append(create_header_data(route_image.title, 3))
        extra_content.append(create_image_data(route_image.image.url, style_class="route_extra_img"))

    context['extra_content'] = render_page_content("[]", extra_content)

    return render(request, 'a4d/routes.html', context)

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

di_5km_text = "1. Uitgang achter SC Hoevelaken rechts op Kerkepad  \n2. Rechtdoor op Kantemarsweg.  \n3. Buig rechtsaf op Westerdorpsstraat.  \n4. Links op Kijftenbeltlaan.  \n5. Links op van Zuylenlaan.  \n6. Rechts op van Lyndenlaan.  \n7. Rechts op Sportweg  \n8. Rechts op voetpad Stoutenburgerlaan.  \n9. Rechts op Ibislaan.  \n10. Links op Eiberlaan.  \n11. Rechts op Pluviersingel.  \n12. Rechts op Eiberlaan.  \n13. Links op van Dedemlaan.  \n14.Drinkpause (speeltuin van Dedemlaan) max 15 min  \n15. Rechts op Elzenlaan.  \n16. Buig linksaf op Twaalfmorgenland.  \n17. Volg Twaalfmorgenland.   \n18. Rechts op Pastoorakker.  \n19. Links en volg Pastoorakker.  \n20. Links op Smalle Streek.  \n21. Rechts op Mulderslaantje.  \n22. Links op Westerdorpsstraat.  \n23. Rechts op Hoevelakense Boslaan.  \n24. Rechts en volg Hoevelakense Boslaan.  \n25. Rechts op fietspad Veenwal.  \n26. Rechts en volg Veenwal.  \n27. Buig rechtsaf en volg Veenwal.  \n28. Buig rechtsaf op Kerkepad.  \n29. Rechts achter ingang SC Hoevelaken"
wo_5km_text = "1. Uitgang achter SC Hoevelaken links op Kerkepad  \n2. Rechts op Veenwal  \n3. Rechts op Lievevrouwepad  \n4. Links op Weteringpad.  \n5. Rechtdoor op Veenlanden  \n6. Rechts op ’t Viertel  \n7. Links op de Lagebrinkerweg  \n8. Links op De Hilt  \n9. Rechts op Veenlanden  \n10. Links en volg Veenlanden  \n11. Rechts op Hogebrinkerweg  \n12. Links op Oosterdorpsstraat  \n13. Rotonde oversteken  \n14. Rechts op Koninginneweg (fietspad op)  \n15. Rechtdoor op Bessel van Butselerlaan.  \n16. Rechts op Doctor F.W. Klaarenbeeksingel.  \n17. Drinkpause (Speeltuin F.W. Klaarenbeeksingel) max 15 min  \n18. Rechts op Wouter van de Glindlaan  \n19. Oversteek Koninginneweg  \n20. Rechts op Horstweg.  \n21. Links op Prinsenhof.  \n22 Rechts op Nassaulaan.  \n23. Rechts op Julianalaan.  \n24. Links op Oosterdorpsstraat.  \n25. Rechts op Huisstede.  \n26. Links en volg Huisstede.  \n27. Links op Veenlanden.  \n28. Rechts op Weteringpad.  \n29. Rechts op Weidelaan.  \n30. Rechts op Veenslagenweg. \n31. Kruising Grasmaat Veenslagenweg  \n32. Rechts op Kleinhovenweg.  \n33. Rechts op Kerkepad.  \n34. Links ingang SC Hoevelaken"


def route_info_5km(request):
    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()],
        'title': 'Routes 5km',
        'img_di': '',
        'img_wo': '',
        'img_do': '',
        'img_vr': '',
        'di_route': list(),
        'wo_route': list(),
        'do_route': list(),
        'vr_route': list(),
    }

    routes = [
        (1, 'di_route', 'img_di'),
        (2, 'wo_route', 'img_wo'),
        (3, 'do_route', 'img_do'),
        (4, 'vr_route', 'img_vr'),
    ]

    for var_set in routes:
        route: Route = Route.get_route(var_set[0])
        if route:
            if route.description:
                context[var_set[1]] = route.description.splitlines()
            if (route.image):
                context[var_set[2]] = route.image.url

    return render(request, 'a4d/route_info.html', context)

def route_info_10km(request):
    context = {
        'menu': get_menu(),
        'thanx': [o.name for o in ThanxToModel.objects.all()],
        'title': 'Routes 10km',
        'img_di': '',
        'img_wo': '',
        'img_do': '',
        'img_vr': '',
        'di_route': list(),
        'wo_route': list(),
        'do_route': list(),
        'vr_route': list(),
    }

    routes = [
        (5, 'di_route', 'img_di'),
        (6, 'wo_route', 'img_wo'),
        (7, 'do_route', 'img_do'),
        (8, 'vr_route', 'img_vr'),
    ]

    for var_set in routes:
        route: Route = Route.get_route(var_set[0])
        if route:
            if route.description:
                context[var_set[1]] = route.description.splitlines()
            if (route.image):
                context[var_set[2]] = route.image.url

    return render(request, 'a4d/route_info.html', context)
