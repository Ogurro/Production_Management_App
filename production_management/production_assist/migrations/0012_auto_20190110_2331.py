# Generated by Django 2.1.4 on 2019-01-10 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0011_auto_20190110_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['-id']},
        ),
    ]
