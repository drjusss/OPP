from apps.api import models


def serialize_augmented_user(augmented_user: models.AugmentedUser) -> dict:
    return {
        'id': augmented_user.pk,
        'name': augmented_user.name,
        'email': augmented_user.email,
        'amount_completed_tasks': augmented_user.amount_completed_tasks,
        'amount_running_tasks': augmented_user.amount_running_tasks,
    }


def serialize_appeal(appeal: models.Appeal) -> dict:
    if appeal.worker:
        worker ={
            'id': appeal.worker.pk,
            'name': appeal.worker.name,
        }

    else:
        worker = None

    return {
        'pk': appeal.pk,
        'name': appeal.name,
        'skype': appeal.skype,
        'message': appeal.message,
        'headset': appeal.headset,
        'sound_is_ok': appeal.sound_is_ok,
        'date_of_group_start': appeal.date_of_group_start,
        'worker': worker,
        'lead_time': appeal.lead_time,
        'is_completed': appeal.is_completed,
        'camera': appeal.camera,
        'speed_test': appeal.speed_test,
        'speed_test_note': appeal.speed_test_note,
        'student_note': appeal.student_note,
        'appeal_type': appeal.appeal_type,
    }


def serialize_appeal_to_unauthorized_user(appeal: models.Appeal) -> dict:
    return {
        'name': appeal.name,
        'skype': appeal.skype,
        'message': appeal.message,
    }
