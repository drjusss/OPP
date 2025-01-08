from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator

from apps.api import models
from apps.api.utils.serializers import serialize_engineer, serialize_manager
from apps.api.utils import decorators


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
class PersonalDataView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        engineer = models.Engineer.objects.filter(user=request.user).first()  # type: ignore
        manager = models.Manager.objects.filter(user=request.user).first()  # type: ignore

        if engineer is not None:
            data = serialize_engineer(engineer=engineer)
            data['role'] = 'engineer'
        elif manager is not None:
            data = serialize_manager(manager)
            data['role'] = 'manager'
        else:
            return JsonResponse(data={'error': 'Not found'}, status=404)

        return JsonResponse(data=data, status=200)
