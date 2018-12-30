from django.contrib import admin
from .models import (
    Company,
    Person,
    Material,
    Retail,
    Offer,
)

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Material)
admin.site.register(Retail)
admin.site.register(Offer)
