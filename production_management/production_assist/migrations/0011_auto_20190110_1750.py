# Generated by Django 2.1.4 on 2019-01-10 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0010_auto_20190109_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name', 'company']},
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='person',
            name='position',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
