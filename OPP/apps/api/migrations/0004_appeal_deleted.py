# Generated by Django 5.0.6 on 2024-06-11 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_massage_appeal_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='appeal',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
    ]
