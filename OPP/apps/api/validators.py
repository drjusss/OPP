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

