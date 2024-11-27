import typing
import json
from functools import wraps

from django.http import HttpRequest, HttpResponse, JsonResponse

from apps.api.utils.model import augmented_user as augmented_user_utils


def check_authorized_decorator(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return JsonResponse(data={'error': 'Not authorized.'}, status=401)
        return func(request=request, *args, **kwargs)

    return wrapper


def validate_json(json_validation_func: typing.Callable, data_validation_func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром data(dict | list)"""
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            data = json.load(request)
            # TODO: добавить проверку лишних значений в функциях валидации json
            json_is_valid, error_message = json_validation_func(data=data)
            if not json_is_valid:
                return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

            data_is_valid, error_message = data_validation_func(**data)
            if not data_is_valid:
                return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

            return func(request=request, data=data, *args, **kwargs)

        return wrapper
    return decorator


def validate_credential_json(json_validation_func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром data(dict | list)"""
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            data = json.load(request)

            json_is_valid, error_message = json_validation_func(data=data)
            if not json_is_valid:
                return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

            return func(request=request, data=data, *args, **kwargs)
        return wrapper
    return decorator


def check_for_nonempty_request(get_func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром appeal(dict | list)"""
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
            appeal = get_func(pk=pk)
            if appeal is None:
                return JsonResponse(data={'error': 'The appeal does not exist'}, status=404)
            return func(request=request, appeal=appeal, *args, **kwargs)
        return wrapper
    return decorator


def get_augmented_user_by_token(func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром augmented_user(AugmentedUser)"""
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        token = request.GET.get('token')
        if token is None:
            return JsonResponse(data={'error': 'Miss token.'}, status=400)

        augmented_user = augmented_user_utils.get(token=token)
        if augmented_user is None:
            return JsonResponse(data={'error': 'The link is outdated.'}, status=400)

        response = func(request=request, augmented_user=augmented_user, *args, **kwargs)
        return response
    return wrapper
