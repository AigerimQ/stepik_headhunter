"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from conf.views import MainView
from jobs.views import VacanciesView, SpecializationVacanciesView, CompanyView, VacancyView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('/vacancies', VacanciesView.as_view(), name='vacancies'),
    path('/vacancies/cat/frontend', SpecializationVacanciesView.as_view(), name='specialization'),
    path('/companies/345', CompanyView.as_view(), name='company'),
    path('/vacancies/22', VacancyView.as_view(), name='vacancy'),
    path('admin/', admin.site.urls),
]
