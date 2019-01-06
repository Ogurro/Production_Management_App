from django.shortcuts import render, get_object_or_404
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


def get_page_range(page_number, page_end):
    """
    Prepares range context for pagination in template
    :param page_number: actual page number of None
    :param page_end: maximum number of pages by default should be *context['page_obj'].paginator.num_pages + 1*
    :return: range(page_start, page_end), length of 10 if possible
    """
    try:
        page_number = int(page_number)
    except TypeError:
        page_number = 1
    page_start = page_number - 4 if page_number > 5 else 1
    if page_end >= 10 and page_start == 1:
        page_end = 10
    elif page_end > 10:
        page_end = page_number + 5 if page_number + 5 <= page_end else page_end
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
        page_number = self.request.GET.get('page')
        page_end = context['page_obj'].paginator.num_pages + 1
        context['page_range'] = get_page_range(page_number, page_end)
        return context


class CompanyDetailView(DeleteView):
    template_name = 'production_assist/company-detail-view.html'
    queryset = Company.objects.all()

    def get_object(self, queryset=queryset):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Company, id=id_)
