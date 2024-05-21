from . import models


def serialize_augmented_user(augmented_user: models.AugmentedUser) -> dict:
    return {
        'pk': augmented_user.pk,
        'email': augmented_user.email,
        'amount_completed_tasks': augmented_user.amount_completed_tasks,
        'amount_running_tasks': augmented_user.amount_running_tasks,
    }


def serialize_appeal(appeal: models.Appeal) -> dict:
    if appeal.worker:
        worker = appeal.worker.pk
    else:
        worker = None

    return {
        'pk': appeal.pk,
        'name': appeal.name,
        'skype': appeal.skype,
        'massage': appeal.massage,
        'headset': appeal.headset,
        'soundIsOk': appeal.sound_is_ok,
        'dateOfGroupStart': appeal.date_of_group_start,
        'worker': worker,
        'leadTime': appeal.lead_time,
        'isComplete': appeal.is_complete,
    }

