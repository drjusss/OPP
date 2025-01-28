import datetime

from apps.api import models
from django.core.exceptions import ObjectDoesNotExist
from . import augmented_user as augmented_user_utils


def get(pk: int | None = None, skype: str | None = None) -> models.Appeal | None:
    try:
        if pk:
            return models.Appeal.objects.get(pk=pk)
        if skype:
            return models.Appeal.objects.get(skype=skype)
    except ObjectDoesNotExist:
        return None


def update(
    appeal: models.Appeal,
    headset: bool | None,
    sound_is_ok: bool | None,
    date_of_group_start: datetime.datetime | None,
    worker: models.Engineer,
    to_complete: bool | None = None,
    camera: bool | None = None,
    type: str | None = None,
    connection_type: str | None = None,
    time_to_complete: str | None = None,
    speed_test: str | None = None,
    speed_test_note: str | None = None,
    student_note: str | None = None,
) -> None:

    if headset is not None:
        appeal.headset = headset

    if sound_is_ok is not None:
        appeal.sound_is_ok = sound_is_ok

    if date_of_group_start is not None:
        appeal.date_of_group_start = date_of_group_start

    if to_complete is not None:
        appeal.is_completed = to_complete

    if camera is not None:
        appeal.camera = camera

    if type is not None:
        appeal.type = type

    if connection_type is not None:
        appeal.type_of_connection = connection_type

    if time_to_complete is not None:
        appeal.time_to_complete = time_to_complete

    if speed_test is not None:
        appeal.speed_test = speed_test

    if speed_test_note is not None:
        appeal.speed_test_note = speed_test_note

    if student_note is not None:
        appeal.student_note = student_note

    if worker != appeal.worker:
        if appeal.worker is not None:
            augmented_user_utils.decrement_amount_running_tasks(augmented_user=appeal.worker)
        appeal.worker = worker
        augmented_user_utils.increment_amount_running_tasks(augmented_user=worker)
    appeal.save()


def change_complete_status(appeal: models.Appeal, to_complete: bool) -> None:
    appeal.is_completed = to_complete
    appeal.save()


def change_delete_status(appeal: models.Appeal, deleted: bool) -> None:
    appeal.deleted = deleted
    appeal.save()


def change_spam_status(appeal: models.Appeal, is_spam: bool) -> None:
    appeal.is_spam = is_spam
    appeal.save()


def create(name: str, skype: str, message: str) -> models.Appeal:
    appeal = models.Appeal(name=name, skype=skype, message=message)
    appeal.save()

    return appeal


def filter_query_set(is_completed_filter_value: str, worker_id_filter_value: str, appeal_date_filter_value: str, appeal_type_filter_value: str, search_filter_value: str, start_date: datetime, end_date:datetime) -> models.models.QuerySet:
    appeals = models.Appeal.objects.filter(is_spam=False, is_deleted=False, date_of_create__range=(start_date, end_date))

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
        appeals = appeals.filter(pk__icontains=search_filter_value) | appeals.filter(
            name__icontains=search_filter_value) | appeals.filter(
            skype__icontains=search_filter_value) | appeals.filter(message__icontains=search_filter_value)

    return appeals


def filter_appeals_by_date(start_date: datetime, end_date: datetime) -> models.models.QuerySet:
    appeals = models.Appeal.objects.filter(date_of_create__range=(start_date, end_date))
    return appeals


def check_date_format(start_date: str, end_date: str) -> [bool, 'str | [datetime.datetime, datetime.datetime]']:
    if start_date is None:
        return False, 'start_date undefined'
    if end_date is None:
        return False, 'end_date undefined'

    try:
        start_date_object = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return False, 'Invalid date format of start_date param'
    try:
        end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return False, 'Invalid date format of end_date param'

    return True, [start_date_object, end_date_object]
