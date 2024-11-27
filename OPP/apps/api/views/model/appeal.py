import datetime
import json

from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from apps.api.utils.model import appeal as appeal_utils, augmented_user as augmented_user_utils
from apps.api.utils import general as general_utils, serializers, decorators, validators
from apps.api import models


@method_decorator(name='post', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_create_appel, data_validation_func=validators.validate_data_to_create_appeal))
@method_decorator(name='patch', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_change_appeal_complete_status, data_validation_func=validators.validate_data_to_change_appeal_complete_status))
@method_decorator(name='delete', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_delete_or_restore_appeals, data_validation_func=validators.validate_data_to_delete_or_restore_appeals))
class AppealsApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        appeals = models.Appeal.objects.filter(is_deleted=False, is_spam=False).order_by('-pk')  # order_by - отсортировать по, добавить фильтр на is_spam=False
        page_size = int(request.GET.get('page-size', default=100))
        page_id = int(request.GET.get('page-id', default=1))

        appeals_by_page = general_utils.get_data_by_page(  # пагинация
            data=appeals,
            page_id=page_id,
            page_size=page_size
        )

        response_data = [serializers.serialize_appeal(appeal=appeal) for appeal in appeals_by_page]
        return JsonResponse(data=response_data, safe=False, status=200)  # Если передаёшь список в качестве джейсона, то нужно указывать safe=False.

    def post(self, request: HttpRequest, data: dict | list) -> HttpResponse:
        appeal = appeal_utils.create(
            name=data['name'],
            skype=data['skype'],
            message=data['message']
        )
        response_data = {
            'result': 'New appeal successfully has been created!',
            'data': serializers.serialize_appeal_to_unauthorized_user(appeal=appeal),
        }
        return JsonResponse(data=response_data, status=201)

    def patch(self, request: HttpRequest, data: dict | list) -> HttpResponse:
        appeal_ids = data['ids']
        to_complete = data['to_complete']

        appeals = [appeal_utils.get(pk=appeal_id) for appeal_id in appeal_ids]

        for appeal in appeals:
            appeal_utils.change_complete_status(
                appeal=appeal,
                to_complete=to_complete
            )

        return JsonResponse(data={'result': 'The appeals was successfully updated'}, status=200)

    def delete(self, request: HttpRequest, data: dict | list) -> HttpResponse:
        appeal_ids = data['ids']
        deleted = data['deleted']

        appeals = [appeal_utils.get(pk=appeal_id) for appeal_id in appeal_ids]

        for appeal in appeals:
            appeal_utils.change_delete_status(
                appeal=appeal,
                deleted=deleted
            )

        return JsonResponse(data={'result': 'The appeals was successfully deleted'}, status=200)


@method_decorator(name='put', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_update_appeal, data_validation_func=validators.validate_data_to_update_appeal))
@method_decorator(name='patch', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_complete_appeal, data_validation_func=validators.validate_data_to_complete_appeal))
@method_decorator(name='delete', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_delete_appeal, data_validation_func=validators.validate_data_to_change_delete_and_spam_status))
@method_decorator(name='dispatch', decorator=decorators.check_for_nonempty_request(get_func=appeal_utils.get))
class AppealApiView(View):
    def get(self, request: HttpRequest, appeal: models.Appeal) -> HttpResponse:
        response_data = serializers.serialize_appeal(appeal=appeal)

        return JsonResponse(data=response_data, status=200)

    def put(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> HttpResponse:
        headset = data.get('headset')
        sound_is_ok = data.get('sound_is_ok')
        date_of_group_start = data.get('date_of_group_start')
        worker_id = data.get('worker_id')
        to_complete = data.get('to_complete')
        camera = data.get('camera')
        appeal_type = data.get('appeal_type')

        worker = augmented_user_utils.get(pk=worker_id)
        if worker is None:
            return JsonResponse(data={'error': ' The worker does not exist.'}, status=404)

        if date_of_group_start is not None:
            date_of_group_start = datetime.datetime.strptime(date_of_group_start, '%d.%m.%Y')

        appeal_utils.update(
            appeal=appeal,
            headset=headset,
            sound_is_ok=sound_is_ok,
            date_of_group_start=date_of_group_start,
            worker=worker,
            to_complete=to_complete,
            camera=camera,
            appeal_type=appeal_type,
        )
        return JsonResponse(data={'result': 'The appeal was successfully updated.'}, status=200)

    def patch(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> HttpResponse:
        to_complete = data['to_complete']
        appeal_utils.change_complete_status(appeal=appeal, to_complete=to_complete)

        return JsonResponse(data={'result': 'The appeal was successfully updated.'}, status=200)

    def delete(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> HttpResponse:
        if data['command'] == 'delete':
            appeal_utils.change_delete_status(appeal=appeal, deleted=True)
        else:
            appeal_utils.change_spam_status(appeal=appeal, is_spam=True)

        return JsonResponse(data={'result': 'The appeal was successfully updated.'}, status=200)


@method_decorator(name='put', decorator=decorators.check_authorized_decorator)
@method_decorator(name='delete', decorator=decorators.check_authorized_decorator)
class AppealForAugmentedUserView(View):
    def put(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> JsonResponse:
        augmented_user = augmented_user_utils.get(user=request.user)

        appeal_utils.update(appeal=appeal, headset=None, sound_is_ok=None, date_of_group_start=None, worker=augmented_user)
        return JsonResponse(data={'result': 'The worker was successfully updated.'}, status=200)

    def delete(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> JsonResponse:
        augmented_user = augmented_user_utils.get(user=request.user)
        if augmented_user != appeal.worker:
            return JsonResponse(data={'result': 'Object does not exist.'}, status=404)
        # appeal_utils.update(appeal=appeal, headset=None, sound_is_ok=None, date_of_group_start=None, worker=None)
        return JsonResponse(data={'result': 'The worker was successfully deleted.'}, status=200)


class FixiksApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        fixiks_obj = models.AugmentedUser.objects.all()
        response_data = [serializers.serialize_augmented_user(augmented_user=fixik) for fixik in fixiks_obj]

        return JsonResponse(data=response_data, safe=False, status=200)

#TODO:
#TODO: