import datetime
import csv

from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.utils.decorators import method_decorator

from apps.api.utils.model import appeal as appeal_utils, augmented_user as augmented_user_utils
from apps.api.utils import general as general_utils, serializers, decorators, validators
from apps.api import models


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='delete', decorator=decorators.check_authorized_decorator)
@method_decorator(name='delete', decorator=decorators.check_user_is_engineer)
@method_decorator(name='post', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_create_appel, data_validation_func=None))
@method_decorator(name='delete', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_delete_or_restore_appeals, data_validation_func=validators.validate_data_to_delete_or_restore_appeals))
class AppealsApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        start_date = request.GET.get('start-date')
        if start_date is None:
            return JsonResponse(data=list(), safe=False, status=200)

        try:
            start_date_object = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            return JsonResponse(data={'error': 'Invalid date format of start_date param'}, status=400)

        end_date = request.GET.get('end-date')
        if end_date is None:
            return JsonResponse(data=list(), safe=False, status=200)

        try:
            end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # end_date_object = end_date_object.replace(hour=23, minute=59, second=59)  # если было поле DateTimeField
        except ValueError:
            return JsonResponse(data={'error': 'Invalid date format of end_date param'}, status=400)

        appeals_by_date = appeal_utils.filter_appeals_by_date(start_date=start_date_object, end_date=end_date_object)

        response_data = [serializers.serialize_appeal(appeal=appeal) for appeal in appeals_by_date]
        return JsonResponse(data=response_data, safe=False, status=200)  # Если передаёшь список в качестве джейсона, то нужно указывать safe=False.

    def post(self, request: HttpRequest, data: dict | list) -> HttpResponse:
        appeal = appeal_utils.create(name=data['name'], skype=data['skype'], message=data['message'])

        response_data = {
            'result': 'New appeal successfully has been created!',
            'data': serializers.serialize_appeal_to_unauthorized_user(appeal=appeal),
        }

        return JsonResponse(data=response_data, status=201)

    def delete(self, request: HttpRequest, data: dict | list) -> HttpResponse:
        appeal_ids = data['ids']
        deleted = data['deleted']

        appeals = [appeal_utils.get(pk=appeal_id) for appeal_id in appeal_ids]

        for appeal in appeals:
            appeal_utils.change_delete_status(appeal=appeal, deleted=deleted)

        return JsonResponse(data={'result': 'The appeals was successfully deleted'}, status=200)


@method_decorator(name='dispatch', decorator=decorators.check_authorized_decorator)
@method_decorator(name='put', decorator=decorators.check_user_is_engineer)
@method_decorator(name='delete', decorator=decorators.check_user_is_engineer)
@method_decorator(name='put', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_update_appeal, data_validation_func=validators.validate_data_to_update_appeal))
@method_decorator(name='delete', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_delete_appeal, data_validation_func=None))
@method_decorator(name='dispatch', decorator=decorators.check_object_exist(get_func=appeal_utils.get))
class AppealApiView(View):
    def get(self, request: HttpRequest, appeal: models.Appeal) -> HttpResponse:
        response_data = serializers.serialize_appeal(appeal=appeal)

        return JsonResponse(data=response_data, status=200)

    def put(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> HttpResponse:
        date_of_group_start = data.get('date_of_group_start')
        worker_id = data.get('worker_id')

        worker = augmented_user_utils.get(pk=worker_id)
        if worker is None:
            return JsonResponse(data={'error': ' The worker does not exist.'}, status=404)

        if date_of_group_start is not None:
            date_of_group_start = datetime.datetime.strptime(date_of_group_start, '%d.%m.%Y')

        appeal_utils.update(
            appeal=appeal,
            headset=data.get('headset'),
            sound_is_ok=data.get('sound_is_ok'),
            date_of_group_start=date_of_group_start,
            worker=worker,
            to_complete=data.get('to_complete'),
            camera=data.get('camera'),
            type=data.get('type'),
            connection_type=data.get('connection_type'),
            time_to_complete=data.get('time_to_complete'),
            speed_test=data.get('speed_test'),
            speed_test_note=data.get('speed_test_note'),
            student_note=data.get('student_note'),
        )
        return JsonResponse(data={'result': 'The appeal was successfully updated.'}, status=200)

    def delete(self, request: HttpRequest, data: dict | list, appeal: models.Appeal) -> HttpResponse:
        if data['command'] == 'delete':
            appeal_utils.change_delete_status(appeal=appeal, deleted=True)
        else:
            appeal_utils.change_spam_status(appeal=appeal, is_spam=True)

        return JsonResponse(data={'result': 'The appeal was successfully updated.'}, status=200)


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='get', decorator=decorators.check_user_is_engineer)
class FixiksApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        fixiks_obj = models.Engineer.objects.all()
        response_data = [serializers.serialize_augmented_user(augmented_user=fixik) for fixik in fixiks_obj]

        return JsonResponse(data=response_data, safe=False, status=200)


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='get', decorator=decorators.check_user_is_engineer)
@method_decorator(name='get', decorator=decorators.validate_get_request_to_export_appeals(query_params_validation_func=None, data_validation_func=validators.validate_data_to_export_appeals))
class ExportAppealsToCSVView(View):
    def get(self, request: HttpRequest) -> FileResponse:
        os_type = request.GET.get('os', 'windows')

        if os_type == 'windows':
            os_type_encoding = 'windows-1251'
        else:
            os_type_encoding = 'utf-8'

        now = datetime.datetime.now()
        verbose_now = datetime.datetime.strftime(now, format='%d.%m.%Y %H.%M.%S')
        file_name = f'./export/{verbose_now}.csv'

        filtered_appeals = appeal_utils.filter(
            is_completed_filter_value=request.GET.get('is-completed'),
            worker_id_filter_value=request.GET.get('worker-id'),
            appeal_type_filter_value=request.GET.get('appeal-type'),
            appeal_date_filter_value=request.GET.get('appeal-date'),
            search_filter_value=request.GET.get('search'),
        )

        appeals = list(filtered_appeals)
        appeals.sort(key=lambda obj: obj.name.lower())

        with open(file=file_name, mode='w', encoding=os_type_encoding) as file:
            writer = csv.writer(file, delimiter=';')
            headers = ['Имя', 'Скайп', 'Гарнитура', 'Тип подключения', 'Звук', 'Камера', 'Скорость инета/пинг', 'Дата старта', 'Кто сделал']
            writer.writerow(headers)

            for appeal in appeals:
                if appeal.worker is None:
                    worker = '-'
                else:
                    worker = appeal.worker.name

                writer.writerow([appeal.name, appeal.skype, appeal.headset, appeal.type_of_connection, appeal.headset, appeal.camera, appeal.speed_test, appeal.date_of_group_start, worker])

        response = FileResponse(open(file=file_name, mode='rb'))  # as_attachment чтобы дать понять что мы отправляем файл, который нужно скачать

        return response


#TODO: отрефакторить бэк
#TODO: пагинация?

#TODO: