import json
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from . import models, serializers, utils, validators, decorators


# @method_decorator(decorator=decorators.check_authorized_decorator, name='get')
# @method_decorator(decorator=decorators.check_authorized_decorator, name='patch')
# @method_decorator(decorator=decorators.check_authorized_decorator, name='delete')
class AppealsApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        appeals = models.Appeal.objects.all()
        page_size = int(request.GET.get('page-size', default=5))
        page_id = int(request.GET.get('page-id', default=1))
        appeals_by_page = utils.get_data_by_page(data=appeals, page_id=page_id, page_size=page_size)  # пагинация
        response_data = [serializers.serialize_appeal(appeal=appeal) for appeal in appeals_by_page]
        return JsonResponse(data=response_data, safe=False, status=200)

    def post(self, request: HttpRequest) -> HttpResponse:
        data = json.load(request)  # загрузить данные из request

        json_is_valid, error_message = validators.validate_json_to_create_appel(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

        data_is_valid, error_message = validators.validate_data_to_create_appeal(data=data)
        if not data_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_message}, status=400)

        appeal = models.Appeal(
            name=data['name'],
            skype=data['skype'],
            message=data['message'],
        )
        appeal.save()
        response_data = {
            'result': 'New appeal successfully has been created!',
            'data': serializers.serialize_appel_to_unauthorized_user(appeal=appeal),
        }
        return JsonResponse(data=response_data, status=201)

    def patch(self, request: HttpRequest) -> HttpResponse:
        data = json.load(request)
        id_appeals = data['ids']
        pass
    def delete(self, request: HttpRequest) -> HttpResponse:
        data = json.load(request)
        id_appeals = data['ids']


class AppealApiView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def put(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass
