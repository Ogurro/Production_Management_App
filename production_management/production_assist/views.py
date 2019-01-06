from django.shortcuts import render
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
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


class LogoutView(auth_views.LogoutView):
    def make_success_message(self):
        messages.success(self.request, f'{str(self.request.user).capitalize()} is logged out')
        return True

    def dispatch(self, request, *args, **kwargs):
        self.make_success_message()
        super(LogoutView, self).dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'production_assist/login-view.html'

    def get_success_message(self, cleaned_data):
        self.success_message = f'Logged in as {str(self.request.user).capitalize()}'
        return self.success_message % cleaned_data


class CompanyListView(ListView):
    template_name = 'production_assist/company-detail-view.html'
    queryset = Company.objects.all()
    paginate_by = 25
