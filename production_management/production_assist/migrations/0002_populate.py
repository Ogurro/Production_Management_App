# Generated by Django 2.1.4 on 2018-12-30 14:32

from django.db import migrations
from production_assist.models import *
from faker import Factory as FakerFactory
import random
import datetime

fake = FakerFactory.create('pl_PL')


def materials():
    material = [
        'Steel',
        'Stainless Steel',
        'Ceramic',
        'Polietylen']
    for mat in material:
        Material.objects.create(type=mat)
    return True


def companies():
    for _ in range(4):
        name = fake.company()
        email = f'{name[0:10]}@mail.com'.replace(' ', '.')
        Company.objects.create(name=name, email=email)
    return True


def persons():
    company = Company.objects.all()
    for c in company:
        for _ in range(3):
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone = fake.phone_number()
            Person.objects.create(first_name=first_name,
                                  last_name=last_name,
                                  phone=phone,
                                  company=c
                                  )
    return True


def retails():
    company = Company.objects.all()
    material = Material.objects.all()
    for c in company:
        for _ in range(4):
            r = Retail()
            r.name = fake.word()
            r.description = fake.sentence()
            r.company = c
            r.material = random.choice(material)
            r.thickness = random.randint(1, 200)
            r.width = random.randint(1, 1000)
            r.length = random.randint(r.width, 2000)
            r.save()
    return True


def offers():
    company = Company.objects.all()
    for c in company:
        person = Person.objects.filter(company=c)
        for _ in range(3):
            o = Offer()
            o.company = c
            o.person = random.choice(person)
            o.manufacture = random.choice([True, False])
            o.final_date = fake.date_between_dates(date_start=datetime.date.today(),
                                                   date_end=datetime.date(2100, 12, 31)
                                                   )
            o.save()
            o.number = f'O-{str(o.id).zfill(5)}'
            o.save()
    return True


def offerretail():
    offer = Offer.objects.all()
    for o in offer:
        retail = Retail.objects.filter(company=o.company)
        retail_set = random.sample(set(retail), random.randint(1, len(retail)))
        for r in retail_set:
            of_re = OfferRetail()
            of_re.offer = o
            of_re.retail = r
            of_re.quantity = random.randint(1, 1000)
            of_re.save()
    return True


def populate(apps, schema_editor):
    materials()
    companies()
    persons()
    retails()
    offers()
    offerretail()


class Migration(migrations.Migration):
    dependencies = [
        ('production_assist', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]
