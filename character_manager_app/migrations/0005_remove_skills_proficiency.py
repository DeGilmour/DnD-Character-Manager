# Generated by Django 3.2.9 on 2021-11-15 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character_manager_app', '0004_auto_20211115_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skills',
            name='proficiency',
        ),
    ]