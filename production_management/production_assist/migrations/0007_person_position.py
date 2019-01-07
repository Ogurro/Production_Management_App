# Generated by Django 2.1.4 on 2019-01-06 22:58

from django.db import migrations, models
from . import populate


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0006_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunPython(populate),
    ]