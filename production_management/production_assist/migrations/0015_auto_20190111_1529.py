# Generated by Django 2.1.5 on 2019-01-11 14:29

from django.db import migrations, models
import django.db.models.deletion
from . import populate


class Migration(migrations.Migration):
    dependencies = [
        ('production_assist', '0014_auto_20190111_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, default='')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production_assist.Offer')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='RetailInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, default='')),
                ('retail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production_assist.Retail')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='companydetails',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RunPython(populate),
    ]
