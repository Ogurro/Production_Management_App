# Generated by Django 2.1.5 on 2019-01-11 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0016_auto_20190111_1718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['status', '-id']},
        ),
    ]
