from django.db import models
from django.urls import reverse_lazy


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('company-detail-view', kwargs={'id': self.id})


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    phone = models.IntegerField()

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

    def get_absolute_url(self):
        return reverse_lazy('material-detail-view', kwargs={'id': self.id})


class Retail(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    thickness = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    cutting_length = models.IntegerField()
    cutting_time = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['company', 'name', 'thickness', ]

    def __str__(self):
        return f'{self.name} #{self.thickness} {self.width}x{self.length}'

    def get_absolute_url(self):
        return reverse_lazy('retail-detail-view', kwargs={'id': self.id})


class Offer(models.Model):
    number = models.CharField(max_length=7)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, null=True)
    retail = models.ManyToManyField(Retail, null=True)
    manufacture = models.BooleanField(default=False)
    final_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id', ]

    def save(self, *args, **kwargs):
        self.number = f'{self.id}'.zfill(5)
        self.number = f'O-{self.number}'
        super(Offer, self).save(*args, **kwargs)
