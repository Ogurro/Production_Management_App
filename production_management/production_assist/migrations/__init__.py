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
    ]
    for mat in material:
        Material.objects.create(type=mat)
    return True


def companies():
    for _ in range(4):
        name = fake.company()
        Company.objects.create(name=name)
    return True


def companies_details():
    company = Company.objects.all()
    for c in company:
        obj = CompanyDetails(company=c)
        obj.email = fake.address()
        obj.phone = fake.phone_number()
        obj.address = fake.email()
        obj.save()
    return True


def persons():
    company = Company.objects.all()
    for c in company:
        for _ in range(3):
            obj = Person(company=c)
            obj.first_name = fake.first_name()
            obj.last_name = fake.last_name()
            obj.phone = fake.phone_number()
            obj.save()
    return True


def retails():
    company = Company.objects.all()
    material = Material.objects.all()
    for c in company:
        for _ in range(4):
            obj = Retail(company=c)
            obj.name = fake.word()
            obj.description = fake.sentence()
            obj.material = random.choice(material)
            obj.thickness = fake.random_int(min=1, max=100)
            obj.width = fake.random_int(min=10, max=1000)
            obj.length = fake.random_int(min=10, max=2000)
            if obj.width > obj.length:
                obj.width, obj.length = obj.length, obj.width
            obj.save()
    return True


def offers():
    company = Company.objects.all()
    for c in company:
        person = Person.objects.filter(company=c)
        for _ in range(3):
            obj = Offer(company=c)
            obj.person = random.choice(person)
            obj.manufacture = fake.boolean()
            obj.final_date = fake.date_between_dates(date_start=datetime.date.today(),
                                                     date_end=datetime.date(2100, 12, 31)
                                                     )
            obj.save()
            obj.number = f'O-{str(obj.id).zfill(5)}'
            obj.save()
    return True


def offerretail():
    offer = Offer.objects.all()
    for o in offer:
        retail = Retail.objects.filter(company=o.company)
        retail_set = random.sample(set(retail), random.randint(1, len(retail)))
        for r in retail_set:
            obj = OfferRetail(offer=o, retail=r)
            obj.quantity = fake.random_int(min=1, max=1000)
            obj.save()
    return True


def populate(*args, **kwargs):
    materials()
    companies()
    companies_details()
    persons()
    retails()
    offers()
    offerretail()
