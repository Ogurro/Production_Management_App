from django.db import models
from django.urls import reverse_lazy
from django.db.models import Q

OFFER_STATUS = (
    (-1, 'Reclamation'),
    (0, 'Registered'),
    (1, 'Project'),
    (2, 'Pricing'),
    (3, 'Production'),
    (4, 'Tooling'),
    (5, 'Ready to receive'),
    (6, 'Finished'),
    (7, 'On hold'),
)


class CompanyModelManager(models.Manager):
    def search(self, name=None, email=None, phone=None, address=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=name)) if name else queryset
        queryset = queryset.filter(Q(companydetails__email__icontains=email)) if email else queryset
        queryset = queryset.filter(Q(companydetails__phone__icontains=phone)) if phone else queryset
        queryset = queryset.filter(Q(companydetails__address__icontains=address)) if address else queryset
        return queryset.distinct()


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = CompanyModelManager()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('company-detail-view', kwargs={'id_company': self.id})


class CompanyDetails(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=32, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.company.name}: {self.address}'


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    phone = models.CharField(max_length=32, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    position = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['last_name', 'company']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse_lazy('company-person-detail-view', kwargs={'id_company': self.company_id, 'id_person': self.id})


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
    description = models.TextField(blank=True, default='')
    thickness = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    cutting_length = models.IntegerField(blank=True, default=0)
    cutting_time = models.IntegerField(blank=True, default=0)
    drawing_number = models.CharField(max_length=255, blank=True, default='')
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, default=0)

    class Meta:
        ordering = ['company', '-id', 'name', 'thickness', ]

    def __str__(self):
        return f'{self.name} #{self.thickness} {self.width}x{self.length}'

    def get_absolute_url(self):
        return reverse_lazy('company-retail-detail-view', kwargs={'id_company': self.company_id, 'id_retail': self.id})


class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, null=True, blank=True)
    retail = models.ManyToManyField(Retail, through='OfferRetail')
    manufacture = models.BooleanField(default=False)
    final_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=OFFER_STATUS, default=0)

    class Meta:
        ordering = ['status', '-id', ]

    def __str__(self):
        return f'O-{str(self.id).zfill(6)}'

    def get_absolute_url(self):
        return reverse_lazy('company-offer-detail-view', kwargs={'id_company': self.company_id, 'id_offer': self.id})


class OfferRetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    retail = models.ForeignKey(Retail, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = (('offer', 'retail'),)

    def __str__(self):
        return f'{self.offer}  {self.retail.name}'

    def get_absolute_url(self):
        return reverse_lazy('company-offer-detail-view',
                            kwargs={'id_company': self.offer.company_id, 'id_offer': self.offer_id})


class RetailInformation(models.Model):
    retail = models.ForeignKey(Retail, on_delete=models.PROTECT)
    info = models.TextField(blank=True, default='')
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.info}'


class OfferInformation(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    info = models.TextField(blank=True, default='')
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.info}'
