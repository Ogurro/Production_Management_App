# Generated by Django 2.1.4 on 2019-01-06 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_assist', '0004_offer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
