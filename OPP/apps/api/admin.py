from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.AugmentedUser)
class AugmentedUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'email', 'token', 'amount_completed_tasks', 'amount_running_tasks']
    list_display_links = ['pk', 'user']


@admin.register(models.Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'skype', 'message', 'headset', 'sound_is_ok', 'date_of_group_start', 'worker', 'lead_time', 'speed_test', 'speed_test_note', 'camera', 'is_completed', 'is_deleted', 'type', 'is_spam', 'type_of_connection', 'time_to_complete']
    list_display_links = ['pk', 'name']
    list_per_page = 10
    list_filter = ['is_completed', 'sound_is_ok', 'headset', 'worker', 'is_deleted']  # Фильтрация по полям
    search_fields = ['pk', 'skype', 'date_of_group_start']  # Поиск по таблице


@admin.register(models.Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'user', 'email']
    list_display_links = ['pk', 'name', 'user', 'email']
