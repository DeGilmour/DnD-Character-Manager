# Generated by Django 3.2.9 on 2021-11-15 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.IntegerField()),
                ('proficiency', models.BooleanField(null=True)),
            ],
        ),
    ]