# Generated by Django 2.1.4 on 2019-01-08 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0007_person_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetails',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='companydetails',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
