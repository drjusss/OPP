import secrets

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from apps.api import models


def get(pk: int | None = None, username: str | None = None, token: str | None = None, user: User | None = None) -> models.Engineer | None:
    try:
        if pk is not None:
            return models.Engineer.objects.get(pk=pk)
        if username is not None:
            return models.Engineer.objects.get(email=username)
        if token is not None:
            return models.Engineer.objects.get(token=token)
        if user is not None:
            return models.Engineer.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


def increment_amount_running_tasks(augmented_user: models.Engineer) -> None:
    augmented_user.amount_running_tasks += 1
    augmented_user.save()


def decrement_amount_running_tasks(augmented_user: models.Engineer) -> None:
    augmented_user.amount_running_tasks -= 1
    augmented_user.save()
