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
)

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home-view'),
    re_path(r'^company/$', CompanyListView.as_view(), name='company-list-view'),
    re_path(r'^company/(?P<id>(\d)+)/$', CompanyDetailView.as_view(), name='company-detail-view'),
    re_path(r'^login/$', LoginView.as_view(), name='login-view'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout-view'),
    re_path(r'^admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
