from functools import wraps
from django.urls import reverse, resolve


def is_authenticated(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'request' in kwargs:
            request = kwargs['request']
        else:
            request = args[0]

        if hasattr(request, 'user'):
            if request.user.is_authenticated:
                return func(*args, **kwargs)
        return resolve(reverse('a4d_login')).func(request)
    return inner
