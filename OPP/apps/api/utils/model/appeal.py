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
    skype: str | None,
    headset: bool | None,
    sound_is_ok: bool | None,
    date_of_group_start: datetime.datetime | None,
    worker: models.AugmentedUser | None
) -> None:

    if skype is not None:
        appeal.skype = skype
    if headset is not None:
        appeal.headset = headset
    if sound_is_ok is not None:
        appeal.sound_is_ok = sound_is_ok
    if date_of_group_start is not None:
        appeal.date_of_group_start = date_of_group_start
    if worker is not None:
        appeal.worker = worker
        augmented_user_utils.increment_amount_running_tasks(augmented_user=worker)
    appeal.save()


def change_complete_status(appeal: models.Appeal, to_complete: bool) -> None:
    appeal.is_complete = to_complete
    appeal.save()


def change_delete_status(appeal: models.Appeal, deleted: bool) -> None:
    appeal.deleted = deleted
    appeal.save()

