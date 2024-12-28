import datetime
import json
import csv
import os.path
import uuid
from wsgiref.util import FileWrapper

from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http.request import QueryDict

from apps.api.utils.model import appeal as appeal_utils, augmented_user as augmented_user_utils
from apps.api.utils import general as general_utils, serializers, decorators, validators
from apps.api import models


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='patch', decorator=decorators.check_authorized_decorator)
@method_decorator(name='delete', decorator=decorators.check_authorized_decorator)
@method_decorator(name='patch', decorator=decorators.check_user_is_engineer)
@method_decorator(name='delete', decorator=decorators.check_user_is_engineer)
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


@method_decorator(name='dispatch', decorator=decorators.check_authorized_decorator)
@method_decorator(name='put', decorator=decorators.check_user_is_engineer)
@method_decorator(name='patch', decorator=decorators.check_user_is_engineer)
@method_decorator(name='delete', decorator=decorators.check_user_is_engineer)
@method_decorator(name='put', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_update_appeal, data_validation_func=validators.validate_data_to_update_appeal))
@method_decorator(name='patch', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_complete_appeal, data_validation_func=validators.validate_data_to_complete_appeal))
@method_decorator(name='delete', decorator=decorators.validate_json(json_validation_func=validators.validate_json_to_delete_appeal, data_validation_func=validators.validate_data_to_change_delete_and_spam_status))
@method_decorator(name='dispatch', decorator=decorators.check_object_exist(get_func=appeal_utils.get))
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
        type = data.get('type')
        connection_type = data.get('connection_type')
        time_to_complete = data.get('time_to_complete')
        speed_test = data.get('speed_test')
        speed_test_note = data.get('speed_test_note')
        student_note = data.get('student_note')

        print(speed_test)
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
            type=type,
            connection_type=connection_type,
            time_to_complete=time_to_complete,
            speed_test=speed_test,
            speed_test_note=speed_test_note,
            student_note=student_note,
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


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='get', decorator=decorators.check_user_is_engineer)
class FixiksApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        fixiks_obj = models.AugmentedUser.objects.all()
        response_data = [serializers.serialize_augmented_user(augmented_user=fixik) for fixik in fixiks_obj]

        return JsonResponse(data=response_data, safe=False, status=200)


@method_decorator(name='get', decorator=decorators.check_authorized_decorator)
@method_decorator(name='get', decorator=decorators.check_user_is_engineer)
@method_decorator(name='get', decorator=decorators.validate_get_request_to_export_appeals(query_params_validation_func=validators.validate_query_dict_to_export_appeals, data_validation_func=validators.validate_data_to_export_appeals))
class ExportAppealsToCSVView(View):
    def get(self, request: HttpRequest) -> FileResponse:
        os_type = request.GET.get('os', 'windows')

        is_completed_filter_value = request.GET.get('is-completed')
        worker_id_filter_value = request.GET.get('worker-id')
        appeal_type_filter_value = request.GET.get('appeal-type')
        appeal_date_filter_value = request.GET.get('appeal-date')
        search_filter_value = request.GET.get('search')

        if os_type == 'windows':
            os_type_encoding = 'windows-1251'
        else:
            os_type_encoding = 'utf-8'

        now = datetime.datetime.now()
        verbose_now = datetime.datetime.strftime(now, format='%d.%m.%Y %H.%M.%S')
        file_name = f'./export/{verbose_now}.csv'

        with open(file=file_name, mode='w', encoding=os_type_encoding) as file:
            writer = csv.writer(file, delimiter=';')
            headers = ['Имя', 'Скайп', 'Гарнитура', 'Тип подключения', 'Звук', 'Камера', 'Скорость инета/пинг', 'Дата старта', 'Кто сделал']
            writer.writerow(headers)
            appeals = models.Appeal.objects.filter(is_spam=False, is_deleted=False)

            if is_completed_filter_value is not None:
                is_completed = is_completed_filter_value.lower() == 'true'
                appeals = appeals.filter(is_completed=is_completed)

            if worker_id_filter_value is not None:
                worker_pk = int(worker_id_filter_value)
                appeals = appeals.filter(worker__pk=worker_pk)

            if appeal_date_filter_value is not None:
                appeal_date = datetime.datetime.strptime(appeal_date_filter_value, '%Y-%m-%d').date()
                appeals = appeals.filter(date_of_group_start=appeal_date)

            if appeal_type_filter_value is not None:
                appeals = appeals.filter(type=appeal_type_filter_value)

            if search_filter_value is not None:
                search_filter_value = search_filter_value.lower()
                # appeals_by_pk = appeals.filter(pk__icontains=search_filter_value)
                # appeals_by_name = appeals.filter(name__icontains=search_filter_value)
                # appeals_by_skype = appeals.filter(skype__icontains=search_filter_value)
                # appeals_by_message = appeals.filter(message__icontains=search_filter_value)

                # appeals = appeals.filter(Q(pk__icontains=search_filter_value) | Q(name__icontains=search_filter_value) | Q(skype__icontains=search_filter_value) | Q(message__icontains=search_filter_value))
                appeals = appeals.filter(pk__icontains=search_filter_value) | appeals.filter(name__icontains=search_filter_value) | appeals.filter(skype__icontains=search_filter_value) | appeals.filter(message__icontains=search_filter_value)

            appeals = list(appeals)
            appeals.sort(key=lambda appeal: appeal.name.lower())

            for appeal in appeals:
                if appeal.worker is None:
                    worker = '-'
                else:
                    worker = appeal.worker.name

                writer.writerow([appeal.name, appeal.skype, appeal.headset, appeal.type_of_connection, appeal.headset, appeal.camera, appeal.speed_test, appeal.date_of_group_start, worker])

        response = FileResponse(open(file=file_name, mode='rb'))  # as_attachment чтобы дать понять что мы отправляем файл, который нужно скачать

        # with open(file=file_name, mode='rb') as file:
            # file_content = FileWrapper(file) # content_type - нужен чтобы передать фронту формат данных
        # response['content-disposition'] = f'attachment; filename={verbose_now}.csv'  # Именуем файл через такой способ
            # response['content-length'] = os.path.getsize(file_name)  # Принимаем путь до файла и возвращае5м его размер

        return response


#TODO: отрефакторить бэк
#TODO:

# https://flowbite.com/docs/components/alerts/ - алерты, если они у нас где-то останутся
# https://flowbite.com/docs/components/buttons/ - кнопки, возможно стоит взять готовый вариант с ховерами и везде где есть - заменить
# https://flowbite.com/docs/components/card/ - карта регистрации и возможно вариант для карточек?
# https://flowbite.com/docs/components/datepicker/ - красивый календарь
# https://flowbite.com/docs/components/dropdowns/ - для селектов?
# https://flowbite.com/docs/components/forms/ - или это для регистрации?
# https://flowbite.com/docs/components/modal/ - или это вариант для карточки?
# https://flowbite.com/docs/components/pagination/ - пагинация, она же будет?
# https://flowbite.com/docs/components/tables/ - однозначно на замену таблицы из 2005
# https://flowbite.com/docs/components/tabs/ - возможно для будушего чтобы переходить в дашборд и профиль
# https://flowbite.com/docs/components/toast/ - типо алерта только успешного?
# https://flowbite.com/docs/forms/input-field/ - красивые инпуты
# https://flowbite.com/docs/forms/search-input/ - инпут для поиска?
# https://flowbite.com/docs/forms/select/ - красивые селекты
# https://flowbite.com/docs/forms/textarea/ - красивая textarea
# https://flowbite.com/docs/forms/checkbox/ - у нас всего 1 чекбокс но мб понадобится
# https://flowbite.com/docs/forms/floating-label/ - движущиеся лейблы, выглядит неплохо
# https://flowbite.com/docs/plugins/datatables/ - понравились фильтры для таблицы

# https://flowbite.com/docs/customize/dark-mode/ - очень бы хотелось иметь темную тему...