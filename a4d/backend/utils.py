from functools import wraps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from typing import Optional


def allow_zero(func):
    func.allow_zero = True
    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return inner_wrapper

class DetailApiView(APIView):

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """

        if not(hasattr(self, 'model') and hasattr(self, 'keyword') and hasattr(self, 'id_name')):
            raise RuntimeError(
                'While using DetailApiView you must set the `model`, `keyword` and `id_name` attribute'
            )

        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            if self.id_name not in kwargs:
                raise Exception(f'{self.id_name} not found in the request')

            try:
                object_set = False
                if hasattr(handler, 'allow_zero'):
                    if handler.allow_zero:
                        if kwargs[self.id_name] == 0:
                            object = None
                            object_set = True
                if not object_set:
                    object = self.model.objects.get(id=kwargs[self.id_name])
                del kwargs[self.id_name]
                kwargs[self.keyword] = object
                response = handler(request, *args, **kwargs)
            except self.model.DoesNotExist:
                response = Response(status=404)


        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

def create_header_data(text: str, size: int):
    return {
            'id': 'gen-header',
            'type': 'header',
            'data': {
                'level': size,
                'text': text
            }
        }

def create_image_data(url: str, style_class: Optional[str] = None):
    data = {
        'id': 'gen-image',
        'type': 'image',
        'data': {
            'url': url
        }
    }
    if (style_class):
        data["data"]["html_class"] = style_class

    return data

def create_text_data(text: str):
    return {
        'id': 'gen-paragraph',
        'type': 'paragraph',
        'data': {
            'text': text
        }
    }