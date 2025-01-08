from apps.api import models


def serialize_augmented_user(augmented_user: models.Engineer) -> dict:
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
        'type': appeal.type,
        'type_of_connection': appeal.type_of_connection,
        'time_to_complete': appeal.time_to_complete,
    }


def serialize_appeal_to_unauthorized_user(appeal: models.Appeal) -> dict:
    return {
        'name': appeal.name,
        'skype': appeal.skype,
        'message': appeal.message,
    }


def serialize_engineer(engineer: models.Engineer) -> dict:
    return {
        'name': engineer.name,
        'email': engineer.email,
        'amount_completed_tasks': engineer.amount_completed_tasks,
        'amount_running_tasks': engineer.amount_running_tasks,
    }


def serialize_manager(manager: models.Manager) -> dict:
    return {
        'name': manager.name,
        'email':manager.email,
    }