# Generated by Django 2.1.4 on 2018-12-31 09:34

from django.db import migrations
from . import populate


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0002_auto_20181231_0934'),
    ]

    operations = [
        migrations.RunPython(populate)
    ]