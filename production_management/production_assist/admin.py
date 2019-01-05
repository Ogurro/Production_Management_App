from django.contrib import admin
from .models import (
    Company,
    CompanyDetails,
    Person,
    Material,
    Retail,
    Offer,
    OfferRetail
)

admin.site.register(Company)
admin.site.register(CompanyDetails)
admin.site.register(Person)
admin.site.register(Material)
admin.site.register(Retail)
admin.site.register(Offer)
admin.site.register(OfferRetail)
