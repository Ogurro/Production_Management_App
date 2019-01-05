from django.shortcuts import render
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Company,
    CompanyDetails,
    Person,
    Material,
    Retail,
    Offer,
    OfferRetail
)


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'production_assist/base.html')


class CompanyListView(ListView):
    template_name = 'production_assist/company-detail-view.html'
    queryset = Company.objects.all()
    paginate_by = 25
