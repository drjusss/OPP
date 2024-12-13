import datetime
import re

from django.http import JsonResponse
from django.http.request import QueryDict

from apps.api import models


headset_value_choices = [choice[0] for choice in models.HEADSET_CHOICES]


def validate_augmented_user(email: str) -> None:
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError('Параметр "email" должен быть в формате почты.')


def validate_appeal(name: str, skype: str, headset: str, lead_time: int, is_completed: bool) -> None:
    if not name.isalpha or 3 < len(name) < 20:
        raise ValueError('Параметр "name", должен состоять только из букв и быть длиной от 3 до 19 символов.')

    if not (5 < len(skype) < 36):
        raise ValueError('Параметр skype, должен быть в формате логина скайпа и не более 35 символов.')

    headset_choices = [element[0] for element in models.HEADSET_CHOICES]
    if headset not in headset_choices:
        raise ValueError(f'Параметр "headset" должен быть одним из - {headset_choices}.')

    if lead_time == 0:
        raise ValueError('Параметр "lead_time", должен быть не нулевым.')

    if lead_time and not is_completed:
        raise ValueError('Параметр "is_completed" должен быть установлен "True", если "lead_time" заполнено.')

    if not lead_time and is_completed:
        raise ValueError('Параметр "is_completed" не может быть выполненным, если не заполнен "lead_time".')


def validate_json_to_create_appel(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if set(data.keys()) != {'name', 'skype', 'message'}:
        return False, 'Data must contain only (name, skype, message) keys.'

    if 'name' not in data:
        return False, 'Data must contain "name" key with value string type.'
    if not isinstance(data['name'], str):
        return False, 'The "name" value must be string type.'
    if len(data['name']) == 0:
        return False, 'The "name" value cannot be empty.'
    if len(data['name']) > 60:
        return False, 'The "name" value must be <= 60'

    if 'skype' not in data:
        return False, 'Data must contain "skype" key with value string type.'
    if not isinstance(data['skype'], str):
        return False, 'The "skype" value must be string type.'
    if len(data['skype']) < 5:
        return False, 'The "skype" value must be more than 5 symbols.'

    if 'message' not in data:
        return False, 'Data must contain "message" key with value string type.'
    if not isinstance(data['message'], str):
        return False, 'The "message" value must be string type.'
    if len(data['message']) == 0:
        return False, 'The "message" value cannot be empty.'
    if len(data['message']) > 1000:
        return False, ' The "message" value must be <= 1000'

    return True, str()


def validate_data_to_create_appeal(name: str | None, skype: str | None, message: str | None) -> tuple[bool, str]:
    return True, str()


def validate_json_to_change_appeal_complete_status(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if set(data.keys()) != {'ids', 'to_complete'}:
        return False, 'Data must contain only (ids, to_complete) keys.'

    if 'ids' not in data:
        return False, 'The Json must contain "ids" key with value list[int] type.'
    if not isinstance(data['ids'], list):
        return False, 'The "ids" value must be list[int] type.'
    for number in data['ids']:
        if not isinstance(number, int):
            return False, 'The "ids" values must be "int" type.'

    if 'to_complete' not in data:
        return False, 'The Json must contain "toComplete" key with value "bool" type.'
    if not isinstance(data['to_complete'], bool):
        return False, 'The "to_complete" must be "bool" type.'
    return True, str()


def validate_data_to_change_appeal_complete_status(appeals: list[models.Appeal | None], to_complete: bool) -> tuple[bool, str]:
    if None in appeals:
        return False, 'Some appeals does not exist.'

    return True, str()


def validate_json_to_delete_or_restore_appeals(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if set(data.keys()) != {'ids', 'deleted'}:
        return False, 'Data must contain (ids, deleted) keys only'

    if 'ids' not in data:
        return False, 'The Json must contain "ids" key with value list[int] type.'
    if not isinstance(data['ids'], list):
        return False, 'The "ids" value must be list[int] type.'
    for number in data['ids']:
        if not isinstance(number, int):
            return False, 'The "ids" value must be int type.'

    if 'deleted' not in data:
        return False, 'The Json object must contain "deleted" key with value "bool" type.'
    if not isinstance(data['deleted'], bool):
        return False, 'The "deleted" must be "bool" type.'
    return True, str()


def validate_data_to_delete_or_restore_appeals(appeals: list[models.Appeal | None], deleted: bool) -> tuple[bool, str]:
    if None in appeals:
        return False, 'Some appeals does not exist.'
    return True, str()


def validate_json_to_update_appeal(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if set(data.keys()) != {'headset', 'sound_is_ok', 'date_of_group_start', 'worker_id', 'to_complete', 'camera', 'type', 'connection_type', 'time_to_complete', 'speed_test', 'speed_test_note', 'student_note'}:
        return False, 'Data must contain (skype, headset, sound_is_ok, date_of_group_start, worker_id, to_complete, camera, type, connection_type, time_to_complete, speed_test, speed_test_note, student_note) keys'

    if data['headset'] is not None and data['headset'] not in headset_value_choices:
        return False, f'Data must have "headset" key with value 1 of {headset_value_choices}.'

    if data['sound_is_ok'] is not None and not isinstance(data['sound_is_ok'], bool):
        return False, 'Data must have "sound_is_ok" key, and must be bool type.'

    try:
        if data['date_of_group_start'] is not None:
            datetime.datetime.strptime(data['date_of_group_start'], '%d.%m.%Y')
    except ValueError:
        return False, 'Date of grope start invalid.'

    if not isinstance(data['worker_id'], int):
        return False, 'worker_id value must be int type.'

    if data['worker_id'] <= 0:
        return False, 'Worker id value must be more than 0.'

    if not isinstance(data['to_complete'], bool):
        return False, 'Value to_complete must be "bool" type.'

    if data['camera'] is not None and not isinstance(data['camera'], bool):
        return False, 'Value camera must be "bool" type.'

    return True, str()


def validate_data_to_update_appeal(
    headset: str | None,
    sound_is_ok: bool | None,
    date_of_group_start: str | None,
    worker_id: models.AugmentedUser | None,
    appeal: models.Appeal | None = None,
    to_complete: bool | None = None,
    camera: bool | None = None,
    type: str | None = None,
    connection_type: str | None = None,
    time_to_complete: str | None = None,
    speed_test: str | None = None,
    speed_test_note: str | None = None,
    student_note: str | None = None,
) -> tuple[bool, str]:
    if date_of_group_start is not None:
        date_of_group_start = datetime.datetime.strptime(date_of_group_start, '%d.%m.%Y')

        now = datetime.datetime.now()
        next_year = now.replace(year=now.year + 1)
        previous_year = now.replace(year=now.year - 1)

        if date_of_group_start < previous_year or date_of_group_start > next_year:
            return False, 'Value date of group start must be in range previous year to next year.'

    if headset is None and sound_is_ok is True:
        return False, 'Value Sound is ok cannot be True, if headset is None.'

    return True, str()


def validate_json_to_complete_appeal(data: dict | list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'The Json must be dict type.'

    if 'to_complete' not in data['to_complete']:
        return False, 'Data must contain "to_complete key with value bool type."'
    if not isinstance(data['to_complete'], bool):
        return False, 'To_complete value must be bool type.'

    return True, str()


def validate_data_to_complete_appeal(appeal: models.Appeal, to_complete: bool) -> tuple[bool, str]:
    return True, str()


def validate_json_to_delete_appeal(data: dict | list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'The Json must be dict type.'

    if data['command'] not in ['delete', 'spam']:
        return False, 'Command value must be one of (delete, spam).'

    return True, str()


def validate_data_to_change_delete_and_spam_status(command: str) -> tuple[bool, str]:
    return True, str()


def validate_json_to_sign_up(data: dict | list) -> tuple[bool, str]:
    if set(data.keys()) != {'username', 'password', 'password_confirmation'}:
        return False, 'Data must contain only (username, password, password_confirmation) keys'

    if not ('username' in data and isinstance(data['username'], str)):
        return False, 'Data must contain "username" key with value "str" type.'
    if len(data['username']) < 5:
        return False, 'Username must be more than 4 symbols.'

    if not ('password' in data and isinstance(data['password'], str)):
        return False, 'Data must contain "password" key with value "str" type.'
    if len(data['password']) < 5:
        return False, 'Password must be more than 4 symbols.'

    if not ('password_confirmation' in data and isinstance(data['password_confirmation'], str)):
        return False, 'Data must contain "password_confirmation" key.'

    if data['password'] != data['password_confirmation']:
        return False, 'Password mismatch.'

    if models.AugmentedUser.objects.filter(email=data['username']).first():
        return False, 'Account with this login has already been registered'
    return True, str()


def validate_json_to_sign_in(data: dict | list) -> tuple[bool, str]:
    if 'username' not in data:
        return False, 'Json must contain "username" key.'
    if 'password' not in data:
        return False, 'Json must contain "password" key.'
    return True, str()


def validate_json_to_reset_password(data: dict | list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'
    if 'username' not in data:
        return False, 'Data must contain "username" key with value str type.'
    if len(data['username']) == 0:
        return False, 'Username cannot be empty.'

    return True, str()


def validate_data_to_reset_password(data: dict | list) -> tuple[bool, str]:
    return True, str()


def validate_json_to_update_password(data: dict | list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if 'password' not in data:
        return False, 'Data must contain "password" key'
    if len(data['password']) == 0:
        return False, 'Password cannot be empty.'
    return True, str()


def validate_data_to_update_password(data: dict | list) -> tuple[bool, str]:
    return True, str()


def validate_json_for_employee_assignment(data: dict | list) -> tuple[bool, str]:
    if 'worker_id' not in data:
        return False, 'Data must contain "worker_id" key.'

    if not isinstance(data['worker_id'], int):
        return False, 'Data must have "worker_id" key.'
    if data['worker_id'] <= 0 and data['worker_id'] != -1:
        return False, 'worker_id value must be more than 0 or -1 (if you want to remove worker.).'

    return True, str()


def validate_data_to_employee_assignment(data: dict | list) -> tuple[bool, str]:
    return True, str()


def validate_query_dict_to_export_appeals(data: QueryDict) -> tuple[bool, str]:
    return True, str()


def validate_data_to_export_appeals(data: QueryDict) -> tuple[bool, str]:

    is_completed = data.get('is-completed')
    if is_completed is not None and is_completed.lower() not in ['true', 'false']:
        return False, 'is-completed must be bool type.'

    worker_id = data.get('worker-id')
    if worker_id is not None:
        try:
            int(worker_id)
        except ValueError:
            return False, 'worker-id must be int type'

    appeal_type = data.get('type')
    if appeal_type is not None and appeal_type not in ['incident', 'check']:
        return False, 'Type must be incident or check.'

    date_of_group_start = data.get('date-of-group-start')
    if date_of_group_start is not None:
        try:
            datetime.datetime.strptime(date_of_group_start, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return False, 'date-of-group-start value must be in date format YYYY-mm-dd'

    return True, str()

#TODO
