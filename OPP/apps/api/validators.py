import re
from . import models


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