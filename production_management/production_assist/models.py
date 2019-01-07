from django.db import models
from django.urls import reverse_lazy

OFFER_STATUS = (
    (0, 'Registered'),
    (1, 'Project'),
    (2, 'Pricing'),
    (3, 'Production'),
    (4, 'Tooling'),
    (5, 'Ready to receive'),
    (6, 'Finished'),
    (7, 'On hold'),
    (8, 'Reclamation'),
)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('company-detail-view', kwargs={'id': self.id})


class CompanyDetails(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.company.name}: {self.address}'


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['last_name', ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse_lazy('person-detail-view', kwargs={'id': self.id})


class Material(models.Model):
    type = models.CharField(max_length=255)

    class Meta:
        ordering = ['type', ]

    def __str__(self):
        return f'{self.type}'


class Retail(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    thickness = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    cutting_length = models.IntegerField(null=True, blank=True)
    cutting_time = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['company', 'name', 'thickness', ]

    def __str__(self):
        return f'{self.name} #{self.thickness} {self.width}x{self.length}'

    def get_absolute_url(self):
        return reverse_lazy('retail-detail-view', kwargs={'id': self.id})


class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, null=True, blank=True)
    retail = models.ManyToManyField(Retail, through='OfferRetail')
    manufacture = models.BooleanField(default=False)
    final_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=OFFER_STATUS, default=1)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return f'O-{str(self.id).zfill(6)}'


class OfferRetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    retail = models.ForeignKey(Retail, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.offer}  {self.retail.name}'
