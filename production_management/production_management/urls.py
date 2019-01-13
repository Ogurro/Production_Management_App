"""production_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import re_path, path, include
from production_assist.views import (
    HomeView, LoginView, LogoutView,
    CompanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView,
    PersonListView,
    CompanyPersonListView, CompanyPersonDetailView, CompanyPersonCreateView, CompanyPersonUpdateView,
    RetailListView,
    CompanyRetailListView, CompanyRetailDetailView, CompanyRetailCreateView, CompanyRetailUpdateView,
    OfferListView,
    CompanyOfferListView, CompanyOfferDetailView, CompanyOfferCreateView, CompanyOfferUpdateView,
    OfferRetailCreateView, OfferRetailUpdateView, OfferRetailDeleteView,
    MaterialListView, MaterialCreateView, MaterialUpdateView,
)

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home-view'),

    # COMPANY
    re_path(r'^company/$', CompanyListView.as_view(), name='company-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/$', CompanyDetailView.as_view(), name='company-detail-view'),
    re_path(r'^company/add/$', CompanyCreateView.as_view(), name='company-create-view'),
    re_path(r'^company/edit/(?P<id_company>(\d)+)/$', CompanyUpdateView.as_view(), name='company-update-view'),

    # PERSON
    re_path(r'^person/$', PersonListView.as_view(), name='person-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/$',
            CompanyPersonListView.as_view(), name='company-person-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/(?P<id_person>(\d)+)/$',
            CompanyPersonDetailView.as_view(), name='company-person-detail-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/add/$',
            CompanyPersonCreateView.as_view(), name='company-person-create-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/(?P<id_person>(\d)+)/edit/$',
            CompanyPersonUpdateView.as_view(), name='company-person-update-view'),

    # RETAIL
    re_path(r'^retail/$', RetailListView.as_view(), name='retail-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/retail/$',
            CompanyRetailListView.as_view(), name='company-retail-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/retail/(?P<id_retail>(\d)+)/$',
            CompanyRetailDetailView.as_view(), name='company-retail-detail-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/retail/add/$',
            CompanyRetailCreateView.as_view(), name='company-retail-create-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/retail/(?P<id_retail>(\d)+)/edit/$',
            CompanyRetailUpdateView.as_view(), name='company-retail-update-view'),

    # OFFERS
    re_path(r'^offer/$', OfferListView.as_view(), name='offer-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/offer/$', CompanyOfferListView.as_view(), name='company-offer-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/offer/(?P<id_offer>(\d)+)/$',
            CompanyOfferDetailView.as_view(), name='company-offer-detail-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/offer/add/$',
            CompanyOfferCreateView.as_view(), name='company-offer-create-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/offer/(?P<id_offer>(\d)+)/edit/$',
            CompanyOfferUpdateView.as_view(), name='company-offer-update-view'),

    # OFFER-RETAIL
    re_path(r'^offer/(?P<id_offer>(\d)+)/retail/add/$',
            OfferRetailCreateView.as_view(), name='offer-retail-create-view'),
    re_path(r'^retail/(?P<id_retail>(\d)+)/offer/add/$',
            OfferRetailCreateView.as_view(), name='retail-offer-create-view'),
    re_path(r'^offer/(?P<id_offer>(\d)+)/retail/(?P<id_retail>(\d)+)/edit/$',
            OfferRetailUpdateView.as_view(), name='offer-retail-update-view'),
    re_path(r'^offer/(?P<id_offer>(\d)+)/retail/(?P<id_retail>(\d)+)/delete/$',
            OfferRetailDeleteView.as_view(), name='offer-retail-delete-view'),

    # MATERIAL
    re_path(r'^material/$', MaterialListView.as_view(), name='material-list-view'),
    re_path(r'^material/add/$', MaterialCreateView.as_view(), name='material-create-view'),
    re_path(r'^material/(?P<id_material>(\d)+)/edit/$', MaterialUpdateView.as_view(), name='material-update-view'),

    # ADMIN
    re_path(r'^login/$', LoginView.as_view(), name='login-view'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout-view'),
    re_path(r'^admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
