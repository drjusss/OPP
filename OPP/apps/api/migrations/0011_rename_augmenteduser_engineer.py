# Generated by Django 5.0.6 on 2024-12-28 08:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_manager'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AugmentedUser',
            new_name='Engineer',
        ),
    ]
