# Generated by Django 2.1.4 on 2019-01-11 13:01

from django.db import migrations, models
from . import populate


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0013_auto_20190111_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.IntegerField(choices=[(-1, 'Reclamation'), (0, 'Registered'), (1, 'Project'), (2, 'Pricing'), (3, 'Production'), (4, 'Tooling'), (5, 'Ready to receive'), (6, 'Finished'), (7, 'On hold')], default=1),
        ),
    ]
