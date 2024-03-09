from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, resolve
from django.views.decorators.csrf import csrf_exempt

from a4d.utils import pages_slug_titles
from .forms import LoginForm, UserCreateForm
from .decorators import is_authenticated
from .models import Album


def get_pages(slug):
    pages = [
        [reverse('a4d_beheer'), 'Controlepaneel', bool(slug == 'home')],
        [reverse('a4d_beheer_account'), 'Account', bool(slug == 'account')],
        [reverse('a4d_beheer_users'), 'Beheerders', bool(slug == 'users')],
        [reverse('a4d_beheer_thanx'), 'Bijzondere dank', bool(slug == 'thanx')],
        [reverse('a4d_beheer_album'), 'Foto\'s', bool(slug == 'album')],
        [reverse('a4d_beheer_news'), 'Nieuws', bool(slug == 'news')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'over'}), 'Over', bool(slug == 'over')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'verkeersregelaars'}), 'Verkeersregelaars', bool(slug == 'verkeersregelaars')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'dank'}), 'Dank aan', bool(slug == 'dank')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'sgwb'}), 'SGWB', bool(slug == 'sgwb')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'inschrijven'}), 'Inschrijven', bool(slug == 'inschrijven')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'controles'}), 'Controles', bool(slug == 'controles')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'routes'}), 'Routes', bool(slug == 'routes')],
        [reverse('a4d_beheer_edit', kwargs={'slug': 'parkeren'}), 'Parkeren', bool(slug == 'parkeren')],

    ]


    return pages

@csrf_exempt
def login_page(request) :
    if request.user.is_authenticated:
        return redirect('a4d_beheer')

    next = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)

                next = request.POST.get('next', None)
                if next is not None:
                    return redirect(next)
                else:
                    return redirect('a4d_beheer')
            else:
                form.add_error('password', 'Ongeldig wachtwoord')
    else:
        form = LoginForm()

    context = {'form': form}

    if next is not None:
        context['next'] = next
    elif not request.path.startswith('/login'):
        context['next'] = request.path

    return render(request, 'a4d/backend/login.html', context)

@is_authenticated
def logout_page(request):
    logout(request)
    return redirect('a4d_login')


def home_controll(request):
    if User.objects.all().count() == 0:
        context = {'form': UserCreateForm()}
        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('a4d_login')
            context['form'] = form

        return render(request, 'a4d/backend/startup.html', context)

    if not request.user.is_authenticated:
        return resolve(reverse('a4d_login')).func(request)

    return render(request, 'a4d/backend/home_controll.html', context={'pages': get_pages('home')})

@is_authenticated
def thanx_to_controll(request):
    context = {
        'pages': get_pages('thanx'),
    }

    return render(request, 'a4d/backend/thanx_controll.html', context)


def account_controll(request):
    context = {
        'pages': get_pages('account'),
        'data': {
            'id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
    }

    return render(request, 'a4d/backend/account_controll.html', context)


@is_authenticated
def user_view(request):
    context = {
        'pages': get_pages('users'),
    }

    return render(request, 'a4d/backend/users_controll.html', context)


@is_authenticated
def news_controll(request):
    context = {
        'pages': get_pages('news'),
    }

    return render(request, 'a4d/backend/news_controll.html', context)


@is_authenticated
def edit_page(request, slug):
    valid_slugs = pages_slug_titles.keys()

    if slug not in valid_slugs:
        raise Http404()

    context = {
        'pages': get_pages(slug),
        'slug': slug,
        'title': pages_slug_titles[slug] + ' bewerken'
    }

    return render(request, 'a4d/backend/edit_page_controll.html', context)


@is_authenticated
def album_controll(request):
    context = {
        'pages': get_pages('album')
    }
    return render(request, 'a4d/backend/album_controll.html', context)


@is_authenticated
def gallery_controll(request, slug):
    album = get_object_or_404(Album, slug=slug)

    context = {
        'pages': get_pages('album'),
        'album': album,
        'images': [photo.image.url for photo in album.photos.all()],
    }
    return render(request, 'a4d/backend/gallery_controll.html', context)
