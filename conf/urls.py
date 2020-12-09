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
from django.contrib.auth.views import LogoutView
from django.urls import path

from conf.views import MainView, custom_handler404, custom_handler500
from jobs.views import VacanciesView, SpecializationVacanciesView, CompanyView, VacancyView, ApplicationSendView, \
    MyCompanyView, MyCompanyVacanciesView, MyVacancyView, MyLoginView, RegisterView
from django.conf import settings
from django.conf.urls.static import static

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty>', SpecializationVacanciesView.as_view(), name='specialization'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send',  ApplicationSendView.as_view(), name='application_send'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies', MyCompanyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>', MyVacancyView.as_view(), name='my_vacancy'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
