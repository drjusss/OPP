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
    worker: models.AugmentedUser,
    to_complete: bool | None = None,
    camera: bool | None = None,
    appeal_type: str | None = None,
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
    if appeal_type is not None:
        appeal.appeal_type = appeal_type

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


def create(
    name: str,
    skype: str,
    message: str
) -> models.Appeal:

    appeal = models.Appeal(
        name=name,
        skype=skype,
        message=message,
    )
    appeal.save()
    return appeal

