from datetime import date, datetime, timedelta
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
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
    CompanyPersonCreateForm,
    CompanyRetailCreateForm,
    CompanyOfferCreateForm,
    OfferRetailCreateForm,
    OfferRetailUpdateForm,
    MaterialCreateForm,
    CompanySearchForm,
    PersonSearchForm,
)
from .models import (
    Company,
    CompanyDetails,
    Person,
    Retail,
    Offer,
    OfferRetail,
    Material,
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


# class LogoutView(auth_views.LogoutView):
#     def make_success_message(self):
#         messages.success(self.request, f'{str(self.request.user).capitalize()} is logged out')
#         return True
#
#     def dispatch(self, request, *args, **kwargs):
#         self.make_success_message()
#         return super().dispatch(request, *args, **kwargs)
#
#
# class LoginView(SuccessMessageMixin, auth_views.LoginView):
#     template_name = 'production_assist/login-view.html'
#
#     def get_success_message(self, cleaned_data):
#         self.success_message = f'Logged in as {str(self.request.user).capitalize()}'
#         return super(LoginView, self).get_success_message(cleaned_data)


# COMPANY
class CompanyListView(PaginatedListView):
    template_name = 'production_assist/company-list-view.html'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.GET:
            return Company.objects.all()
        name = self.request.GET.get('name') or ''
        email = self.request.GET.get('email') or ''
        phone = self.request.GET.get('phone') or ''
        address = self.request.GET.get('address') or ''
        return Company.objects.search(name=name, email=email, phone=phone, address=address)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyListView, self).get_context_data()
        search_form = CompanySearchForm(self.request.GET or None)
        context['search_form'] = search_form
        return context


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
        cd = CompanyDetails.objects.get(company=company)
        cd.address = address
        cd.phone = phone
        cd.email = email
        cd.description = description
        cd.save()
        messages.success(self.request, f'Updated company {company}')
        return redirect(company.get_absolute_url())


# PERSON
class PersonListView(PaginatedListView):
    template_name = 'production_assist/person-list-view.html'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.GET:
            return Person.objects.all()
        first_name = self.request.GET.get('first_name') or ''
        last_name = self.request.GET.get('last_name') or ''
        company = self.request.GET.get('company') or ''
        phone = self.request.GET.get('phone') or ''
        email = self.request.GET.get('email') or ''
        position = self.request.GET.get('position') or ''
        return Person.objects.search(first_name=first_name, last_name=last_name, company=company, phone=phone,
                                     email=email, position=position)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PersonListView, self).get_context_data()
        search_form = PersonSearchForm(self.request.GET or None)
        context['search_form'] = search_form
        return context


class CompanyPersonListView(PersonListView):
    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Person.objects.filter(Q(company_id__exact=id_company))


class CompanyPersonDetailView(DetailView):
    template_name = 'production_assist/company-person-detail-view.html'
    queryset = Person.objects.all()

    def get_object(self, queryset=queryset):
        id_person = self.kwargs.get('id_person')
        return get_object_or_404(Person, id=id_person)


class CompanyPersonCreateView(CreateView):
    template_name = 'production_assist/company-person-create-view.html'
    form_class = CompanyPersonCreateForm

    def get_context_data(self, **kwargs):
        context = super(CompanyPersonCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyPersonCreateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        person = form.save()
        messages.success(self.request, f'Added person {person} to company {person.company}')
        return super(CompanyPersonCreateView, self).form_valid(form)


class CompanyPersonUpdateView(UpdateView):
    template_name = 'production_assist/company-person-create-view.html'
    form_class = CompanyPersonCreateForm
    queryset = Person.objects.all()

    def get_object(self, queryset=queryset):
        id_person = self.kwargs.get('id_person')
        return get_object_or_404(Person, id=id_person)

    def get_context_data(self, **kwargs):
        context = super(CompanyPersonUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyPersonUpdateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        person = form.save()
        messages.success(self.request, f'Updated person {person}')
        return super(CompanyPersonUpdateView, self).form_valid(form)


# RETAIL
class RetailListView(PaginatedListView):
    template_name = 'production_assist/retail-list-view.html'
    queryset = Retail.objects.all()
    paginate_by = 15


class CompanyRetailListView(RetailListView):
    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Retail.objects.filter(company_id=id_company)


class CompanyRetailDetailView(DetailView):
    template_name = 'production_assist/company-retail-detail-view.html'
    queryset = Person.objects.all()

    def get_object(self, queryset=queryset):
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(Retail, id=id_retail)


class CompanyRetailCreateView(CreateView):
    template_name = 'production_assist/company-retail-create-view.html'
    form_class = CompanyRetailCreateForm

    def get_context_data(self, **kwargs):
        context = super(CompanyRetailCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyRetailCreateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        retail = form.save()
        messages.success(self.request, f'Added retail {retail} to company {retail.company}')
        return super(CompanyRetailCreateView, self).form_valid(form)


class CompanyRetailUpdateView(UpdateView):
    template_name = 'production_assist/company-retail-create-view.html'
    form_class = CompanyRetailCreateForm
    queryset = Retail.objects.all()

    def get_object(self, queryset=queryset):
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(Retail, id=id_retail)

    def get_context_data(self, **kwargs):
        context = super(CompanyRetailUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyRetailUpdateView, self).get_initial()
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        retail = form.save()
        messages.success(self.request, f'Updated retail {retail}')
        return super(CompanyRetailUpdateView, self).form_valid(form)


# OFFERS
class OfferListView(PaginatedListView):
    template_name = 'production_assist/offer-list-view.html'
    queryset = Offer.objects.all()
    paginate_by = 15


class CompanyOfferListView(OfferListView):
    def get_queryset(self):
        id_company = self.kwargs.get('id_company')
        return Offer.objects.filter(company_id=id_company)


class CompanyOfferDetailView(DetailView):
    template_name = 'production_assist/company-offer-detail-view.html'
    queryset = Offer.objects.all()

    def get_object(self, queryset=queryset):
        id_offer = self.kwargs.get('id_offer')
        return get_object_or_404(Offer, id=id_offer)

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferDetailView, self).get_context_data()
        id_offer = self.kwargs.get('id_offer')
        offer_retails = OfferRetail.objects.filter(Q(offer_id=id_offer))
        context['total_price'] = sum([x.quantity * x.retail.price for x in offer_retails])
        return context


class CompanyOfferCreateView(CreateView):
    template_name = 'production_assist/company-offer-create-view.html'
    form_class = CompanyOfferCreateForm

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferCreateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyOfferCreateView, self).get_initial()
        initial['final_date'] = datetime.strftime(datetime.today() + timedelta(days=7), '%d-%m-%Y')
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        offer = form.save()
        messages.success(self.request, f'Added offer {offer} to company {offer.company}')
        return super(CompanyOfferCreateView, self).form_valid(form)


class CompanyOfferUpdateView(UpdateView):
    template_name = 'production_assist/company-offer-create-view.html'
    form_class = CompanyOfferCreateForm
    queryset = Offer.objects.all()

    def get_object(self, queryset=queryset):
        id_offer = self.kwargs.get('id_offer')
        return get_object_or_404(Offer, id=id_offer)

    def get_context_data(self, **kwargs):
        context = super(CompanyOfferUpdateView, self).get_context_data()
        context['company'] = get_object_or_404(Company, id=self.kwargs.get('id_company'))
        return context

    def get_initial(self):
        initial = super(CompanyOfferUpdateView, self).get_initial()
        id_offer = self.kwargs.get('id_offer')
        offer = get_object_or_404(Offer, id=id_offer)
        initial['final_date'] = date.strftime(offer.final_date, '%d-%m-%Y')
        id_company = self.kwargs.get('id_company')
        initial['company'] = get_object_or_404(Company, id=id_company)
        return initial

    def form_valid(self, form):
        offer = form.save()
        messages.success(self.request, f'Updated offer {offer}')
        return super(CompanyOfferUpdateView, self).form_valid(form)


class OfferRetailCreateView(CreateView):
    template_name = 'production_assist/offer-retail-create-view.html'
    form_class = OfferRetailCreateForm

    def get_context_data(self, **kwargs):
        context = super(OfferRetailCreateView, self).get_context_data()
        id_offer = self.kwargs.get('id_offer')
        if id_offer:
            obj = get_object_or_404(Offer, id=id_offer)
            context['object'] = f'Offer: {obj}'
        else:
            id_retail = self.kwargs.get('id_retail')
            obj = get_object_or_404(Retail, id=id_retail)
            context['object'] = f'Retail: {obj}'
        return context

    def get_initial(self):
        initial = super(OfferRetailCreateView, self).get_initial()
        id_offer = self.kwargs.get('id_offer')
        if id_offer:
            initial['offer'] = get_object_or_404(Offer, id=id_offer)
        else:
            id_retail = self.kwargs.get('id_retail')
            initial['retail'] = get_object_or_404(Retail, id=id_retail)
        return initial

    def form_valid(self, form):
        offerretail = form.save()
        messages.success(self.request, f'Added {offerretail.retail} to {offerretail.offer}')
        return super(OfferRetailCreateView, self).form_valid(form)


class OfferRetailUpdateView(UpdateView):
    template_name = 'production_assist/offer-retail-create-view.html'
    form_class = OfferRetailUpdateForm
    queryset = OfferRetail.objects.all()

    def get_context_data(self, **kwargs):
        context = super(OfferRetailUpdateView, self).get_context_data()
        id_offer = self.kwargs.get('id_offer')
        id_retail = self.kwargs.get('id_retail')
        offer = get_object_or_404(Offer, id=id_offer)
        retail = get_object_or_404(Retail, id=id_retail)
        context['object'] = f'Offer: {offer}'
        context['object2'] = f'Retail: {retail}'
        return context

    def get_object(self, queryset=queryset):
        id_offer = self.kwargs.get('id_offer')
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(OfferRetail, offer_id=id_offer, retail_id=id_retail)

    def form_valid(self, form):
        offerretail = form.save()
        messages.success(self.request, f'Updated {offerretail.retail} in {offerretail.offer}')
        return super(OfferRetailUpdateView, self).form_valid(form)


class OfferRetailDeleteView(DeleteView):
    template_name = 'production_assist/offer-retail-delete-view.html'

    def get_success_url(self):
        obj = self.get_object()
        return obj.offer.get_absolute_url()

    def get_object(self, queryset=None):
        id_offer = self.kwargs.get('id_offer')
        id_retail = self.kwargs.get('id_retail')
        return get_object_or_404(OfferRetail, offer_id=id_offer, retail_id=id_retail)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Deleted {obj.retail} from {obj.offer}')
        return super(OfferRetailDeleteView, self).delete(request, *args, **kwargs)


class MaterialListView(PaginatedListView):
    template_name = 'production_assist/material-list-view.html'
    queryset = Material.objects.all()
    paginate_by = 10


class MaterialCreateView(CreateView):
    template_name = 'production_assist/material-create-view.html'
    form_class = MaterialCreateForm

    def get_success_url(self):
        return reverse_lazy('material-list-view')


class MaterialUpdateView(UpdateView):
    template_name = 'production_assist/material-create-view.html'
    form_class = MaterialCreateForm
    queryset = Material.objects.all()

    def get_object(self, queryset=queryset):
        id_material = self.kwargs.get('id_material')
        return get_object_or_404(Material, id=id_material)

    def get_success_url(self):
        return reverse_lazy('material-list-view')
