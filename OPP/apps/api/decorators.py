import typing
from django.http import HttpRequest, HttpResponse, JsonResponse


def check_authorized_decorator(func: typing.Callable) -> typing.Callable:
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return JsonResponse(data={'error': 'Not authorized.'}, status=401)
        return func(request=request, *args, **kwargs)

    return wrapper
