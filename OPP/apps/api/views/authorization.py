from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout

from apps.api.utils import decorators, validators


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
