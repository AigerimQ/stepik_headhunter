from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class VacanciesView(View):

    def get(self, request):
        return render(request, 'vacancies.html')


class SpecializationVacanciesView(View):

    def get(self, request):
        return render(request, 'vacancies.html')


class CompanyView(View):

    def get(self, request):
        return render(request, 'company.html')


class VacancyView(View):

    def get(self, request):
        return render(request, 'vacancy.html')
