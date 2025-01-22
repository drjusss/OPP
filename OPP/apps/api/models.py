from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

HEADSET_CHOICES = [
    ('USB', 'USB'),
    ('3.5', '3.5'),
    ('USB/3.5', '3.5 наушники и USB микрофон'),
    ('3.5/USB', 'USB наушники и 3.5 микрофон'),
]

TYPE_CHOICES = [
    ('check', 'Проверка'),
    ('incident','Инцидент'),
]

TYPE_OF_CONNECTION = [
    ('wi-fi', 'wi-fi'),
    ('cable', 'кабель'),
]


class Engineer(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, verbose_name='Имя инженера')
    user = models.OneToOneField(to=User, on_delete=models.PROTECT, verbose_name='Встроенный пользователь')  # PROTECT - чтобы нельзя было удалить
    email = models.CharField(max_length=30, unique=True, verbose_name='Почта')
    amount_completed_tasks = models.PositiveIntegerField(default=0, verbose_name='Количество выполненных обращений')
    amount_running_tasks = models.PositiveIntegerField(default=0, verbose_name='Количество текущих обращений')
    token = models.CharField(null=True, blank=True, unique=True, max_length=16, verbose_name='Токен')

    class Meta:
        verbose_name = 'Расширенный пользователь'
        verbose_name_plural = 'Расширенные пользователи'
        db_table = 'augmented_user'


class Manager(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, verbose_name='Имя менеджера')
    user = models.OneToOneField(to=User, on_delete=models.PROTECT, verbose_name='Встроенный пользователь')
    email = models.CharField(max_length=30, unique=True, verbose_name='Почта')

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        db_table = 'manager'


class Appeal(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=60, verbose_name='ФИО ученика')
    skype = models.CharField(max_length=45, verbose_name='Скайп ученика')
    message = models.CharField(max_length=1000, verbose_name='Обращение')
    headset = models.CharField(max_length=10, choices=HEADSET_CHOICES, null=True, blank=True, verbose_name='Гарнитура\микрофон')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True, verbose_name='Тип обращения')
    type_of_connection = models.CharField(max_length=10, choices=TYPE_OF_CONNECTION, null=True, blank=True, verbose_name='Тип подключения')
    sound_is_ok = models.BooleanField(null=True, verbose_name='Звук ученика')
    date_of_group_start = models.DateField(null=True, blank=True, verbose_name='Дата старта группы')
    date_of_create = models.DateField(default=timezone.now, verbose_name='Дата создания')
    worker = models.ForeignKey(to=Engineer, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Кто выполняет')
    lead_time = models.PositiveIntegerField(null=True, blank=True, verbose_name='Время выполнения')
    speed_test = models.CharField(max_length=15, null=True, blank=True, verbose_name='Тест скорости')
    speed_test_note = models.CharField(max_length=200, null=True, blank=True, verbose_name='Комментарий к тесту скорости')
    student_note = models.CharField(max_length=500, null=True, blank=True, verbose_name='Комментарий к ученику')
    camera = models.BooleanField(null=True, blank=True, verbose_name='Камера')
    time_to_complete = models.CharField(max_length=10, null=True, blank=True, verbose_name='Время на проверку')
    is_completed = models.BooleanField(default=False, verbose_name='Завершено')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')
    is_spam = models.BooleanField(default=False, verbose_name='Спам')

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        db_table = 'appeal'
        default_related_name = 'appeals'


