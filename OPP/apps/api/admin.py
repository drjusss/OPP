from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.AugmentedUser)
class AugmentedUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'email', 'amount_completed_tasks', 'amount_running_tasks']
    list_display_links = ['pk', 'user']


@admin.register(models.Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'skype', 'message', 'headset', 'sound_is_ok', 'date_of_group_start', 'worker', 'lead_time', 'is_complete']
    list_display_links = ['pk', 'name']
    list_per_page = 10
    list_filter = ['is_complete', 'sound_is_ok', 'headset', 'worker']  # Фильтрация по полям
    search_fields = ['pk', 'skype', 'date_of_group_start']  # Поиск по таблице
