import datetime
import re
from . import models



headset_value_choices = [choice[0] for choice in models.HEADSET_CHOICES]


def validate_augmented_user(email: str) -> None:
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError('Параметр "email" должен быть в формате почты.')


def validate_appeal(name: str, skype: str, headset: str, lead_time: int, is_complete: bool) -> None:
    if not name.isalpha or 3 < len(name) < 20:
        raise ValueError('Параметр "name", должен состоять только из букв и быть длиной от 3 до 19 символов.')

    if re.match(pattern=r'^[a-zA-Z][a-zA-Z0-9_.,-]{5,31}$', string=skype) or 3 < len(skype) < 36:
        raise ValueError('Параметр skype, должен быть в формате логина скайпа и не более 35 символов.')

    headset_choices = [element[0] for element in models.HEADSET_CHOICES]
    if headset not in headset_choices:
        raise ValueError(f'Параметр "headset" должен быть одним из - {headset_choices}.')

    if lead_time == 0:
        raise ValueError('Параметр "lead_time", должен быть не нулевым.')

    if lead_time and not is_complete:
        raise ValueError('Параметр "is_complete" должен быть установлен "True", если "lead_time" заполнено.')

    if not lead_time and is_complete:
        raise ValueError('Параметр "is_complete" не может быть выполненным, если не заполнен "lead_time".')


def validate_json_to_create_appel(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

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
    if re.match(pattern=r'^[a-zA-Z][a-zA-Z0-9:_.,-]{5,45}$', string=data['skype']) is None:
        return False, 'The "skype" value must be skype login pattern.'

    if 'message' not in data:
        return False, 'Data must contain "message" key with value string type.'
    if not isinstance(data['message'], str):
        return False, 'The "message" value must be string type.'
    if len(data['message']) == 0:
        return False, 'The "message" value cannot be empty.'
    if len(data['message']) > 1000:
        return False, ' The "message" value must be <= 1000'

    return True, str()


def validate_data_to_create_appeal(data: list | dict) -> tuple[bool, str]:
    return True, str()


def validate_json_to_change_appeal_complete_status(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'
    if 'ids' not in data:
        return False, 'The Json must contain "ids" key with value list[int] type.'
    if not isinstance(data['ids'], list):
        return False, 'The "ids" value must be list[int] type.'
    for number in data['ids']:
        if not isinstance(number, int):
            return False, 'The "ids" values must be "int" type.'

    if 'toComplete' not in data:
        return False, 'The Json must contain "toComplete" key with value "bool" type.'
    if not isinstance(data['toComplete'], bool):
        return False, 'The "toComplete" must be "bool" type.'
    return True, str()


def validate_data_to_change_appeal_complete_status(appeals: list[models.Appeal | None], to_complete: bool) -> tuple[bool, str]:
    if None in appeals:
        return False, 'Some appeals does not exist.'

    return True, str()


def validate_json_to_change_appeal_delete_status(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'
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


def validate_data_to_change_appeal_delete_status(appeals: list[models.Appeal | None], deleted: bool) -> tuple[bool, str]:
    if None in appeals:
        return False, 'Some appeals does not exist.'
    return True, str()


def validate_json_to_update_appeal(data: list | dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'Data must be dict type.'

    if 'skype' in data and re.match(pattern=r'^[a-zA-Z][a-zA-Z0-9_.,-]{5,31}$', string=data['skype']) is None:
        return False, 'Data must have "skype" key, and be valid skype login.'
    if 'headset' in data and data['headset'] not in headset_value_choices:
        return False, f'Data must have "headset" key with value 1 of {headset_value_choices}.'
    if 'soundIsOk' in data and not isinstance(data['soundIsOk'], bool):
        return False, 'Data must have "soundIsOk" key, and must be bool type.'
    if 'dateOfGroupStart' in data:
        try:
            datetime.datetime.strptime(data['dateOfGroupStart'], '%d.%m.%Y')
        except ValueError:
            return False, 'Date of grope start invalid.'
    if 'workerId' in data:
        if not isinstance(data['workerId'], int):
            return False, 'Data must have "workerId" key.'
        if data['workerId'] <= 0:
            return False, 'Worker id value must be more than 0.'
    return True, str()


def validate_data_to_update_appeal(
    appeal: models.Appeal | None,
    skype: str | None,
    headset: str | None,
    sound_is_ok: bool | None,
    date_of_group_start: datetime.date | None,
    worker: models.AugmentedUser | None
) -> tuple[bool, str]:

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

    if 'toComplete' not in  data['toComplete']:
        return False, 'Data must contain "toComplete key with value bool type."'
    if not isinstance(data['toComplete'], bool):
        return False, 'ToComplete value must be bool type.'

    return True, str()


def validate_data_to_complete_appeal(appeal: models.Appeal, to_complete: bool) -> tuple[bool, str]:
    return True, str()


def validate_json_to_delete_appeal(data: dict | list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, 'The Json must be dict type.'

    if 'deleted' not in data['deleted']:
        return False, 'Data must contain "deleted" key with value bool type.'
    if not isinstance(data['deleted'], bool):
        return False, 'Deleted value must be bool type.'

    return True, str()


def validate_data_to_delete_appeal(appeal: models.Appeal, deleted: bool) -> tuple[bool, str]:
    return True, str()
