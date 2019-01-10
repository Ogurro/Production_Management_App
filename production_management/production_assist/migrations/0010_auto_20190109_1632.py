# Generated by Django 2.1.4 on 2019-01-09 15:32

from django.db import migrations, models
from . import populate


class Migration(migrations.Migration):
    dependencies = [
        ('production_assist', '0009_auto_20190108_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='retail',
            name='drawing_number',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='retail',
            name='cutting_length',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='retail',
            name='cutting_time',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='retail',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='retail',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20),
        ),
        migrations.RunPython(populate),
    ]