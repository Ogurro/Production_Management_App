from django.shortcuts import render, get_object_or_404, redirect
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

from .forms import (
    CompanyCreateForm,
    CompanyUpdateForm,
)


def get_page_range(request, context):
    page_number = request.GET.get('page')
    page_end = context['page_obj'].paginator.num_pages + 1
    try:
        page_number = int(page_number)
    except TypeError:
        page_number = 1
    page_start = page_number - 3 if page_number > 4 else 1
    if page_end == 10:
        return range(1, 10)
    elif page_end >= 8 and page_start == 1:
        page_end = 8
    elif page_end > 8:
        page_end = page_number + 4 if page_number + 4 <= page_end else page_end
    if page_end - page_start < 7 < page_end:
        page_start = page_end - 7
    return range(page_start, page_end)


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
    template_name = 'production_assist/company-list-view.html'
    queryset = Company.objects.all()
    paginate_by = 15

    def get_context_data(self, *, object_list=queryset, **kwargs):
        context = super(CompanyListView, self).get_context_data()
        context['page_range'] = get_page_range(self.request, context)
        return context


class CompanyDetailView(DetailView):
    template_name = 'production_assist/company-detail-view.html'
    queryset = Company.objects.all()

    def get_object(self, queryset=queryset):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Company, id=id_)


class CompanyCreateView(CreateView):
    template_name = 'production_assist/company-create-view.html'
    form_class = CompanyCreateForm

    def form_valid(self, form):
        company = form.save()
        CompanyDetails.objects.create(company=company)
        submit = self.request.POST.get('save')
        if submit == 'save':
            return redirect(company.get_absolute_url())
        else:
            # TODO make additional info addition
            return redirect(company.get_absolute_url())


class CompanyUpdateView(UpdateView):
    template_name = 'production_assist/company-update-view.html'
    form_class = CompanyUpdateForm
    queryset = Company.objects.all()

    def get_object(self, queryset=queryset):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Company, id=id_)

    def get_initial(self):
        initial = super(CompanyUpdateView, self).get_initial()
        company_details = CompanyDetails.objects.get(company=self.get_object())
        initial['address'] = company_details.address
        initial['phone'] = company_details.phone
        initial['email'] = company_details.email
        return initial

    def form_valid(self, form):
        email = form.cleaned_data.pop('email')
        phone = form.cleaned_data.pop('phone')
        address = form.cleaned_data.pop('address')
        company = form.save()
        company_details = CompanyDetails.objects.get(company=company)
        company_details.address = address
        company_details.phone = phone
        company_details.email = email
        company_details.save()
        return redirect(company.get_absolute_url())
