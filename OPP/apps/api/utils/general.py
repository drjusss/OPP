import typing

from django.contrib.auth.models import User
from apps.api import models


def get_data_by_page(data: list[typing.Any], page_id: int, page_size: int) -> list[typing.Any]:
    start_index = (page_id - 1) * page_size
    stop_index = page_id * page_size
    result = data[start_index:stop_index]
    return result


def get_role_by_user(user: User) -> str | None:
    engineer = models.AugmentedUser.objects.filter(user=user).first()  # type: ignore
    if engineer is not None:
        return 'engineer'

    manager = models.Manager.objects.filter(user=user).first()  # type: ignore
    if manager is not None:
        return 'manager'

    return None
