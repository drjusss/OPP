import datetime
import json
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from .utils.model import appeal as appeal_utils, augmented_user as augmented_user_utils
from .utils import general as general_utils
from . import models, serializers, utils, validators, decorators


# @method_decorator(decorator=decorators.check_authorized_decorator, name='get')
# @method_decorator(decorator=decorators.check_authorized_decorator, name='patch')
# @method_decorator(decorator=decorators.check_authorized_decorator, name='delete')
class AppealsApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        appeals = models.Appeal.objects.all()
        page_size = int(request.GET.get('page-size', default=5))
        page_id = int(request.GET.get('page-id', default=1))
        appeals_by_page = general_utils.get_data_by_page(  # пагинация
            data=appeals,
            page_id=page_id,
            page_size=page_size
        )
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

        json_is_valid, error_massage = validators.validate_json_to_change_appeal_complete_status(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        appeal_ids = data['ids']
        to_complete = data['toComplete']

        appeals = [appeal_utils.get(pk=appeal_id) for appeal_id in appeal_ids]

        data_is_valid, error_massage = validators.validate_data_to_change_appeal_complete_status(
            appeals=appeals,
            to_complete=to_complete
        )
        if not data_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        for appeal in appeals:
            appeal_utils.change_complete_status(
                appeal=appeal,
                to_complete=to_complete
            )

        return JsonResponse(data={'result': 'The appeals was successfully updated'}, status=200)

    def delete(self, request: HttpRequest) -> HttpResponse:
        data = json.load(request)

        json_is_valid, error_massage = validators.validate_json_to_change_appeal_delete_status(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        appeal_ids = data['ids']
        deleted = data['deleted']

        appeals = [appeal_utils.get(pk=appeal_id) for appeal_id in appeal_ids]

        data_is_valid, error_massage = validators.validate_data_to_change_appeal_delete_status(
            appeals=appeals,
            deleted=deleted
        )
        if not data_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        for appeal in appeals:
            appeal_utils.change_delete_status(
                appeal=appeal,
                deleted=deleted
            )

        return JsonResponse(data={'result': 'The appeals was successfully deleted'}, status=200)


class AppealApiView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        appeal = appeal_utils.get(pk=pk)
        if appeal is None:
            return JsonResponse(data={'error': 'The appeal does not exist'}, status=404)

        response_data = serializers.serialize_appeal(appeal=appeal)
        return JsonResponse(data=response_data, status=200)

    def put(self, request: HttpRequest, pk: int) -> HttpResponse:
        appeal = appeal_utils.get(pk=pk)
        if appeal is None:
            return JsonResponse(data={'error': 'The appeal does not exist'}, status=404)
        data = json.load(request)

        json_is_valid, error_massage = validators.validate_json_to_update_appeal(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'Validation error', 'detail': error_massage}, status=400)

        skype = data.get('skype')
        headset = data.get('headset')
        sound_is_ok = data.get('soundIsOk')
        date_of_group_start = data.get('dateOfGroupStart')
        worker_id = data.get('workerId')

        if worker_id is not None:
            worker = augmented_user_utils.get(pk=worker_id)
        else:
            worker = None

        if date_of_group_start is not None:
            date_of_group_start = datetime.datetime.strptime(date_of_group_start, '%d.%m.%Y')

        data_is_valid, error_massage = validators.validate_data_to_update_appeal(
            appeal=appeal,
            skype=skype,
            headset=headset,
            sound_is_ok=sound_is_ok,
            date_of_group_start=date_of_group_start,
            worker=worker,
        )
        if not data_is_valid:
            return JsonResponse(data={'error': 'Validation error', 'detail': error_massage}, status=400)

        appeal_utils.update(
            appeal=appeal,
            skype=skype,
            headset=headset,
            sound_is_ok=sound_is_ok,
            date_of_group_start=date_of_group_start,
            worker=worker,
        )
        return JsonResponse(data='The appeal was successfully updated.', status=200)

    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        appeal = appeal_utils.get(pk=pk)
        if appeal is None:
            return JsonResponse(data={'error': 'The appeal does not exist'}, status=404)
        data = json.load(request)

        json_is_valid, error_massage = validators.validate_json_to_complete_appeal(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        to_complete = data['toComplete']

        data_is_valid, error_massage = validators.validate_data_to_complete_appeal(appeal=appeal, to_complete=to_complete)
        if not data_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        appeal_utils.change_complete_status(appeal=appeal, to_complete=to_complete)
        return JsonResponse(data='The appeal was successfully updated.', status=200)

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        appeal = appeal_utils.get(pk=pk)
        if appeal is None:
            return JsonResponse(data={'error': 'The appeal does not exist'}, status=404)
        data = json.load(request)

        json_is_valid, error_massage = validators.validate_json_to_delete_appeal(data=data)
        if not json_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        deleted = data['deleted']

        data_is_valid, error_massage = validators.validate_data_to_delete_appeal(appeal=appeal, deleted=deleted)
        if not data_is_valid:
            return JsonResponse(data={'error': 'validation error', 'detail': error_massage}, status=400)

        appeal_utils.change_delete_status(appeal=appeal, deleted=deleted)
        return JsonResponse(data='The appeal was successfully updated.', status=200)

