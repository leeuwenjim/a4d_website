# Generated by Django 4.2.9 on 2024-01-28 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_thanxtomodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
    ]
