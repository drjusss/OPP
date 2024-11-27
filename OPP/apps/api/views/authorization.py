import secrets

from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from apps.api.utils import decorators, validators
from apps.api.utils.model import augmented_user as augmented_user_utils
from apps.api import models


@method_decorator(name='post', decorator=decorators.validate_credential_json(json_validation_func=validators.validate_json_to_sign_up))
class SignUpApiView(View):
    def post(self, request: HttpRequest, data: dict | list) -> JsonResponse:
        username = data['username']
        password = data['password']

        user = User.objects.create_user(username=username, password=password)
        user.save()
        augmented_user_utils.create(user=user, username=username)
        login(user=user, request=request)

        return JsonResponse(data={'result': 'Successfully sign up.'}, status=201)

# TODO: дописать валидацию на одинаковых пользователей

@method_decorator(name='post', decorator=decorators.validate_credential_json(json_validation_func=validators.validate_json_to_sign_in))
class SignInApiView(View):
    def post(self, request: HttpRequest, data: dict | list) -> JsonResponse:
        username = data['username']
        password = data['password']

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return JsonResponse(data={'result': 'Invalid credentials.'}, status=400)
        login(user=user, request=request)
        return JsonResponse(data={'result': 'Successfully sign in.'}, status=200)


class SignOutApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        logout(request=request)
        return JsonResponse(data={'result': 'Successfully log out.'})


@method_decorator(name='post', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_reset_password, data_validation_func=validators.validate_data_to_reset_password))
@method_decorator(name='put', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_update_password, data_validation_func=validators.validate_data_to_update_password))
@method_decorator(name='put', decorator=decorators.get_augmented_user_by_token)
@method_decorator(name='get', decorator=decorators.get_augmented_user_by_token)
class ResetPasswordApiView(View):
    def post(self, request: HttpRequest, data: dict | list) -> JsonResponse:
        username = data['username']
        augmented_user = augmented_user_utils.get(username=username)
        if augmented_user is None:
            return JsonResponse(data={'error': 'The User does not exist.'}, status=404)

        new_token = secrets.token_hex(nbytes=8)
        augmented_user.token = new_token
        augmented_user.save()

        print(f'Письмо было отправлено))))) token - {new_token}')
        return JsonResponse(data={'result': 'Check your email.'}, status=200)

    def get(self, request: HttpRequest, augmented_user: models.AugmentedUser) -> JsonResponse:
        return JsonResponse(data={'result': 'Input new password.'}, status=200)

    def put(self, request: HttpRequest, data: dict | list, augmented_user: models.AugmentedUser) -> JsonResponse:
        password = data['password']
        augmented_user.user.set_password(raw_password=password)
        augmented_user.user.save()
        login(user=augmented_user.user, request=request)
        return JsonResponse(data={'result': 'The password was successfully update.'})




