import typing
import json
from functools import wraps

from django.http import HttpRequest, HttpResponse, JsonResponse

from apps.api.utils.model import augmented_user as augmented_user_utils
from apps.api import models


def check_authorized_decorator(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:  # type: ignore
            return JsonResponse(data={'error': 'Not authorized.'}, status=401)
        return func(request=request, *args, **kwargs)

    return wrapper


def check_user_is_engineer(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        augmented_user = models.Engineer.objects.filter(user=request.user).first()  # type: ignore #используем filter/first чтобы не нужно было делать try except(т.к. filter/first вернет None при отсутствие значение, в отличии от get, который вернет ошибку)
        if augmented_user is not None:
            return func(request=request, *args, **kwargs)
        return JsonResponse(data={'error': 'Permission denied.'}, status=403)

    return wrapper


def validate_json(json_validation_func: typing.Callable, data_validation_func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром data(dict | list)"""
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            data = json.load(request)

            json_is_valid, error_message = json_validation_func(data=data)
            if not json_is_valid:
                return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

            data_is_valid, error_message = data_validation_func(**data)
            if not data_is_valid:
                return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

            return func(request=request, data=data, *args, **kwargs)

        return wrapper
    return decorator


def validate_get_request_to_export_appeals(query_params_validation_func: typing.Callable, data_validation_func: typing.Callable) -> typing.Callable:
    """При использовании декоратора, сигнатура функции дополняется параметром data(dict | list)"""
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:

            query_params_is_valid, error_message = query_params_validation_func(request.GET)

            if not query_params_is_valid:
                return HttpResponse(content={'error': 'validation error', 'detail': error_message}, status=400)

            data_is_valid, error_message = data_validation_func(request.GET)
            if not data_is_valid:
                return HttpResponse(content={'error': 'validation error', 'detail': error_message}, status=400)

            return func(request=request, *args, **kwargs)
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


def check_object_exist(get_func: typing.Callable) -> typing.Callable:
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
    """При использовании декоратора, сигнатура функции дополняется параметром augmented_user(Engineer)"""
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
