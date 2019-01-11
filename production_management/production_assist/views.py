from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import (
    CompanyCreateForm,
    CompanyUpdateForm,
    PersonCreateForm,
    CompanyPersonCreateForm,
    RetailCreateForm,
    CompanyRetailCreateForm,
    OfferCreateForm,
    CompanyOfferCreateForm,
)
from .models import (
    Company,
    CompanyDetails,
    Person,
    Retail,
    Offer,
    OfferRetail,
)


class PaginatedListView(ListView):
    """
    Changes ListView to contain page_range for pagination in context
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaginatedListView, self).get_context_data()
        page_number = self.request.GET.get('page')
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
        context['page_range'] = range(page_start, page_end)
        return context


# ADMIN
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


# COMPANY
class CompanyListView(PaginatedListView):
    template_name = 'production_assist/company-list-view.html'
    queryset = Company.objects.all()
    paginate_by = 15


class CompanyDetailView(DetailView):
    template_name = 'production_assist/company-detail-view.html'
    queryset = Company.objects.all()

    def get_object(self, queryset=queryset):
        id_ = self.kwargs.get('id_company')
        return get_object_or_404(Company, id=id_)


class CompanyCreateView(CreateView):
    template_name = 'production_assist/company-create-view.html'
    form_class = CompanyCreateForm

    def form_valid(self, form):
        company = form.save()
        CompanyDetails.objects.create(company=company)
        submit = self.request.POST.get('save')
        messages.success(self.request, f'Added company {company}')
        if submit == 'save':
            return redirect(company.get_absolute_url())
        else:
            return redirect('company-update-view', id_company=company.id)


class CompanyUpdateView(UpdateView):
    template_name = 'production_assist/company-update-view.html'
    form_class = CompanyUpdateForm
    queryset = Company.objects.all()

    def get_object(self, queryset=queryset):
        id_company = self.kwargs.get('id_company')
        return get_object_or_404(Company, id=id_company)

    def get_initial(self):
        initial = super(CompanyUpdateView, self).get_initial()
        company_details = CompanyDetails.objects.get(company=self.get_object())
        initial['address'] = company_details.address
        initial['phone'] = company_details.phone
        initial['email'] = company_details.email
        initial['description'] = company_details.description
        return initial

    def form_valid(self, form):
        email = form.cleaned_data.pop('email')
        phone = form.cleaned_data.pop('phone')
        address = form.cleaned_data.pop('address')
        description = form.cleaned_data.pop('description')
        company = form.save()
        company_details = CompanyDetails.objects.get(company=company)
        company_details.address = address
        company_details.phone = phone
        company_details.email = email
        company_details.description = description
        company_details.save()
        messages.success(self.request, f'Updated company {company}')
        return redirect(company.get_absolute_url())


# PERSON
class PersonListView(PaginatedListView):
    template_name = 'production_assist/person-list-view.html'
    queryset = Person.objects.all()
    paginate_by = 10


class PersonDetailView(DetailView):
    template_name = 'production_assist/person-detail-view.html'
    queryset = Person.objects.all()
    context_object_name = 'person'

    def get_object(self, queryset=queryset):
        id_person = self.kwargs.get('id_person')
        return get_object_or_404(Person, id=id_person)


class PersonCreateView(CreateView):
    template_name = 'production_assist/person-create-view.html'
    form_class = PersonCreateForm

    def get_success_url(self):
        id_person = self.object.id
        person = get_object_or_404(Person, id=id_person)
        return person.get_absolute_url()

    def form_valid(self, form):
        person = form.save()
        messages.success(self.request, f'Added person {person} to company {person.company}')
        return super(PersonCreateView, self).form_valid(form)


class PersonUpdateView(UpdateView):
    template_name = 'production_assist/person-update-view.html'
    form_class = PersonCreateForm
    queryset = Person.objects.all()

    def get_success_url(self):
        id_person = self.object.id
        person = get_object_or_404(Person, id=id_person)
        return person.get_absolute_url()

    def get_object(self, queryset=queryset):
        id_person = self.kwargs.get('id_person')
        return get_object_or_404(Person, id=id_person)

    def form_valid(self, form):
        person = form.save()
        messages.success(self.request, f'Updated person {person}')
        return super(PersonUpdateView, self).form_valid(form)


# COMPANY PERSON
class CompanyPersonListView(PaginatedListView):
    template_name = 'production_assist/company-person-list-view.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyPersonListView, self).get_context_data()
        id_company = self.kwargs.get('id_company')
        context['company'] = get_object_or_404(Company, id=id_company)
        return context

    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Person.objects.filter(company_id=id_company)


class CompanyPersonDetailView(PersonDetailView):
    template_name = 'production_assist/company-person-detail-view.html'


class CompanyPersonCreateView(PersonCreateView):
    template_name = 'production_assist/company-person-create-view.html'
    form_class = CompanyPersonCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyPersonCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyPersonCreateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


class CompanyPersonUpdateView(PersonUpdateView):
    template_name = 'production_assist/company-person-update-view.html'
    form_class = CompanyPersonCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyPersonUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyPersonUpdateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


# RETAIL
class RetailListView(PaginatedListView):
    template_name = 'production_assist/retail-list-view.html'
    queryset = Retail.objects.all()
    paginate_by = 15


class RetailDetailView(DetailView):
    template_name = 'production_assist/retail-detail-view.html'
    queryset = Retail.objects.all()
    context_object_name = 'retail'

    def get_object(self, queryset=queryset):
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(Retail, id=id_retail)


class RetailCreateView(CreateView):
    template_name = 'production_assist/retail-create-view.html'
    form_class = RetailCreateForm

    def get_success_url(self):
        id_retail = self.object.id
        retail = get_object_or_404(Retail, id=id_retail)
        return retail.get_absolute_url()

    def form_valid(self, form):
        retail = form.save()
        messages.success(self.request, f'Added retail {retail} to company {retail.company}')
        return super(RetailCreateView, self).form_valid(form)


class RetailUpdateView(UpdateView):
    template_name = 'production_assist/retail-update-view.html'
    form_class = RetailCreateForm
    queryset = Retail.objects.all()

    def get_success_url(self):
        id_retail = self.object.id
        retail = get_object_or_404(Retail, id=id_retail)
        return retail.get_absolute_url()

    def get_object(self, queryset=queryset):
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(Retail, id=id_retail)

    def form_valid(self, form):
        retail = form.save()
        messages.success(self.request, f'Updated retail {retail}')
        return super(RetailUpdateView, self).form_valid(form)


# COMPANY-RETAIL
class CompanyRetailListView(PaginatedListView):
    template_name = 'production_assist/company-retail-list-view.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyRetailListView, self).get_context_data()
        id_company = self.kwargs.get('id_company')
        context['company'] = get_object_or_404(Company, id=id_company)
        return context

    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Retail.objects.filter(company_id=id_company)


class CompanyRetailDetailView(RetailDetailView):
    template_name = 'production_assist/company-retail-detail-view.html'


class CompanyRetailCreateView(RetailCreateView):
    template_name = 'production_assist/company-retail-create-view.html'
    form_class = CompanyRetailCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyRetailCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyRetailCreateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


class CompanyRetailUpdateView(RetailUpdateView):
    template_name = 'production_assist/company-retail-update-view.html'
    form_class = CompanyRetailCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyRetailUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyRetailUpdateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


# OFFERS
class OfferListView(PaginatedListView):
    template_name = 'production_assist/offer-list-view.html'
    queryset = Offer.objects.all()
    paginate_by = 15


class OfferDetailView(DetailView):
    template_name = 'production_assist/offer-detail-view.html'
    queryset = Offer.objects.all()
    context_object_name = 'offer'

    def get_object(self, queryset=queryset):
        id_offer = self.kwargs.get('id_offer')
        return get_object_or_404(Offer, id=id_offer)


class OfferCreateView(CreateView):
    template_name = 'production_assist/offer-create-view.html'
    form_class = OfferCreateForm

    def get_initial(self):
        initial = super(OfferCreateView, self).get_initial()
        initial['final_date'] = datetime.strftime(datetime.today() + timedelta(days=7), '%d-%m-%Y')
        return initial

    def get_success_url(self):
        id_offer = self.object.id
        offer = get_object_or_404(Offer, id=id_offer)
        return offer.get_absolute_url()

    def form_valid(self, form):
        offer = form.save()
        messages.success(self.request, f'Added offer {offer} to company {offer.company}')
        return super(OfferCreateView, self).form_valid(form)


class OfferUpdateView(UpdateView):
    template_name = 'production_assist/offer-update-view.html'
    form_class = OfferCreateForm
    queryset = Offer.objects.all()

    def get_initial(self):
        initial = super(OfferUpdateView, self).get_initial()
        id_offer = self.kwargs.get('id_offer')
        offer = get_object_or_404(Offer, id=id_offer)
        initial['final_date'] = date.strftime(offer.final_date, '%d-%m-%Y')
        return initial

    def get_success_url(self):
        id_offer = self.object.id
        offer = get_object_or_404(Offer, id=id_offer)
        return offer.get_absolute_url()

    def get_object(self, queryset=queryset):
        id_offer = self.kwargs.get('id_offer')
        return get_object_or_404(Offer, id=id_offer)

    def form_valid(self, form):
        offer = form.save()
        messages.success(self.request, f'Updated offer {offer}')
        return super(OfferUpdateView, self).form_valid(form)


# COMPANY-OFFER
class CompanyOfferListView(PaginatedListView):
    template_name = 'production_assist/company-offer-list-view.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyOfferListView, self).get_context_data()
        id_company = self.kwargs.get('id_company')
        context['company'] = get_object_or_404(Company, id=id_company)
        return context

    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Offer.objects.filter(company_id=id_company)


class CompanyOfferDetailView(OfferDetailView):
    template_name = 'production_assist/company-offer-detail-view.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferDetailView, self).get_context_data()
        id_offer = self.kwargs.get('id_offer')
        offer_retails = OfferRetail.objects.filter(Q(offer_id=id_offer))
        context['total_price'] = sum([x.quantity * x.retail.price for x in offer_retails])
        return context


class CompanyOfferCreateView(OfferCreateView):
    template_name = 'production_assist/company-offer-create-view.html'
    form_class = CompanyOfferCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyOfferCreateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


class CompanyOfferUpdateView(OfferUpdateView):
    template_name = 'production_assist/company-offer-update-view.html'
    form_class = CompanyOfferCreateForm

    def get_success_url(self):
        id_company = self.request.POST.get('company')
        return reverse_lazy('company-detail-view', kwargs={'id_company': id_company})

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyOfferUpdateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial


class OfferRetailCreateView(CreateView):
    pass


class OfferRetailUpdateView(UpdateView):
    pass


class OfferRetailDeleteView(DeleteView):
    pass
