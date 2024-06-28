from django.core.exceptions import ObjectDoesNotExist
from ... import models


def get(pk: int) -> models.AugmentedUser | None:
    try:
        return models.AugmentedUser.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def increment_amount_running_tasks(augmented_user: models.AugmentedUser) -> None:
    augmented_user.amount_running_tasks += 1
    augmented_user.save()