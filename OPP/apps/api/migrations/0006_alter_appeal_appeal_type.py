# Generated by Django 5.0.6 on 2024-11-21 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_appeal_appeal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='appeal_type',
            field=models.CharField(blank=True, choices=[('check', 'Проверка'), ('incident', 'Инцидент')], max_length=10, null=True, verbose_name='Тип обращения'),
        ),
    ]
