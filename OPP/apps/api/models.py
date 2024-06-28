from django.db import models
from django.contrib.auth.models import User
# Create your models here.

HEADSET_CHOICES = [
    ('USB', 'USB'),
    ('3.5', '3.5'),
    ('USB/3.5', '3.5 наушники и USB микрофон'),
    ('3.5/USB', 'USB наушники и 3.5 микрофон'),
]


class AugmentedUser(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(to=User, on_delete=models.PROTECT, verbose_name='Встроенный пользователь')  # PROTECT - чтобы нельзя было удалить
    email = models.CharField(max_length=30, verbose_name='Почта')
    amount_completed_tasks = models.PositiveIntegerField(default=0, verbose_name='Количество выполненных обращений')
    amount_running_tasks = models.PositiveIntegerField(default=0, verbose_name='Количество текущих обращений')

    class Meta:
        verbose_name = 'Расширенный пользователь'
        verbose_name_plural = 'Расширенные пользователи'
        db_table = 'augmented_user'


class Appeal(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=60, verbose_name='ФИО ученика')
    skype = models.CharField(max_length=45, verbose_name='Скайп ученика')
    message = models.CharField(max_length=1000, verbose_name='Обращение')
    headset = models.CharField(max_length=10, choices=HEADSET_CHOICES, null=True, blank=True,  verbose_name='Гарнитура\микрофон')
    sound_is_ok = models.BooleanField(null=True, verbose_name='Звук ученика')
    date_of_group_start = models.DateField(null=True, blank=True, verbose_name='Дата старта группы')
    worker = models.ForeignKey(to=AugmentedUser, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Кто выполняет')
    lead_time = models.PositiveIntegerField(null=True, blank=True, verbose_name='Время выполнения')
    is_complete = models.BooleanField(default=False, verbose_name='Завершено')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        db_table = 'appeal'
        default_related_name = 'appeals'
