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
    HomeView,
    LoginView,
    LogoutView,
    CompanyListView,
    CompanyDetailView,
    CompanyCreateView,
    CompanyUpdateView,
    PersonListView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView,
    CompanyPersonListView,
    CompanyPersonCreateView,
    CompanyPersonUpdateView,
)

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home-view'),

    # company
    re_path(r'^company/$', CompanyListView.as_view(), name='company-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/$', CompanyDetailView.as_view(), name='company-detail-view'),
    re_path(r'^company/add/$', CompanyCreateView.as_view(), name='company-create-view'),
    re_path(r'^company/edit/(?P<id_company>(\d)+)/$', CompanyUpdateView.as_view(), name='company-update-view'),

    # person
    re_path(r'^person/$', PersonListView.as_view(), name='person-list-view'),
    re_path(r'^person/(?P<id_person>(\d)+)/$', PersonDetailView.as_view(), name='person-detail-view'),
    re_path(r'^person/add/$', PersonCreateView.as_view(), name='person-create-view'),
    re_path(r'^person/(?P<id_person>(\d)+)/edit/$', PersonUpdateView.as_view(), name='person-update-view'),

    # company-person
    re_path(r'^company/(?P<id_company>(\d)+)/person/$',
            CompanyPersonListView.as_view(), name='company-person-list-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/add/$',
            CompanyPersonCreateView.as_view(), name='company-person-create-view'),
    re_path(r'^company/(?P<id_company>(\d)+)/person/(?P<id_person>(\d)+)/edit/$',
            CompanyPersonUpdateView.as_view(), name='company-person-update-view'),
    # admin
    re_path(r'^login/$', LoginView.as_view(), name='login-view'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout-view'),
    re_path(r'^admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
