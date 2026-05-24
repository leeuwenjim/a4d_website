"""
URL configuration for a4d project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import frontend.views as frontend_views
from django.conf import settings
import backend.views as backend_views
import backend.api_views as api_views

urlpatterns = [
    # Frontend
    path('', frontend_views.homepage, name='a4d_home'),
    path('favicon.ico', frontend_views.favicon),
    path('nieuws/', frontend_views.nieuws, name='a4d_nieuws'),
    path('nieuws/data/', frontend_views.nieuws_api, name='a4d_nieuws_data'),
    path('fotos/', frontend_views.gallery, name='a4d_gallery'),
    path('fotos/<int:year>/', frontend_views.gallery, name='a4d_gallery_year'),
    path('fotos/<int:year>/<str:day>/', frontend_views.gallery, name='a4d_gallery_day'),
    path('routes/', frontend_views.page_routes, name='a4d_routes'),
    path('routes/5km/', frontend_views.route_info_5km, name='a4d_route_5km'),
    path('routes/10km/', frontend_views.route_info_10km, name='a4d_route_10km'),

    # Controll panel

    path('beheer/', include([
        path('', backend_views.home_controll, name='a4d_beheer'),
        path('login/', backend_views.login_page, name='a4d_login'),
        path('logout/', backend_views.logout_page, name='a4d_logout'),
        path('account/', backend_views.account_controll, name='a4d_beheer_account'),
        path('sponsors/', backend_views.sponsor_control, name='a4d_beheer_sponsors'),
        path('thanx/', backend_views.thanx_to_controll, name='a4d_beheer_thanx'),
        path('users/', backend_views.user_view, name='a4d_beheer_users'),
        path('news/', backend_views.news_controll, name='a4d_beheer_news'),
        path('album/', backend_views.album_controll, name='a4d_beheer_album'),
        path('album/<str:slug>/', backend_views.gallery_controll, name='a4d_beheer_gallery'),
        path('routes/', backend_views.edit_route, name='a4d_beheer_routes'),
        path('routes/description/', backend_views.edit_route_description, name='a4d_beheer_routes_desc'),
        path('<str:slug>/', backend_views.edit_page, name='a4d_beheer_edit'),
    ])),

    # API
    path('api/', include([
        path('users/', api_views.UserView.as_view()),
        path('users/<int:user_id>/', api_views.ManageUserView.as_view()),
        path('albums/', api_views.AlbumOverview.as_view()),
        path('albums/<int:album_id>/', api_views.AlbumDetail.as_view()),
        path('albums/<int:album_id>/images/', api_views.ImageOverview.as_view()),
        path('albums/<int:album_id>/images/<int:photo_id>/', api_views.ImageDetailView.as_view()),
        path('sponsors/', api_views.SponsorOverview.as_view()),
        path('sponsors/<int:sponsor_id>/', api_views.SponsorDetailview.as_view()),
        path('sponsors/<int:sponsor_id>/logo/', api_views.SponsorLogoView.as_view()),
        path('sponsors/<int:sponsor_id>/extra/', api_views.SponsorExtraView.as_view()),
        path('thanx/', api_views.ThanxTo.as_view()),
        path('thanx/<int:t_id>/', api_views.ThanxToDetails.as_view()),
        path('news/', api_views.NewsOverview.as_view()),
        path('news/<int:news_id>/', api_views.NewsDetails.as_view()),
        path('route/', api_views.RouteBaseOverview.as_view()),
        path('route/extra/', api_views.RouteImageOverview.as_view()),
        path('route/extra/<int:img_id>/', api_views.RouteImageDetailView.as_view()),
        path('route/routes/', api_views.RouteOverview.as_view()),
        path('route/routes/<int:route_id>/', api_views.RouteDetailview.as_view()),
        path('route/routes/<int:route_id>/img/', api_views.RouteAttachmentDetailView.as_view()),
        path('<str:slug>/', api_views.PageEditView.as_view()),
    ])),

]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))

urlpatterns.append(path('<str:page>/', frontend_views.page_view, name='a4d_page'))
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
