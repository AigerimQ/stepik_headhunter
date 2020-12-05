from django.http import HttpResponseNotFound
from django.shortcuts import render

from django.views import View

from jobs.models import Vacancy, Specialty, Company


class VacanciesView(View):

    def get(self, request):
        head_title = "Вакансии | "
        title = "Все вакансии"
        vacancies = Vacancy.objects.values('id', 'title', 'skills', 'salary_min', 'salary_max', 'published_at',
                                           'company_id')
        number_of_vacancies = Vacancy.objects.count()
        context = {
            "head_title": head_title,
            "title": title,
            "vacancies": vacancies,
            "number_of_vacancies": number_of_vacancies,
        }

        return render(request, 'vacancies.html', context=context)


class SpecializationVacanciesView(View):

    def get(self, request, specialty):
        head_title = "Вакансии | "
        try:
            title = Specialty.objects.get(code=specialty).title
        except Specialty.DoesNotExist:
            return HttpResponseNotFound('Ой, данная страница не найдена((')

        vacancies = Vacancy.objects.filter(specialty__code=specialty).values('id', 'title', 'skills',
                                                                             'salary_min', 'salary_max', 'published_at',
                                                                             'company_id')
        number_of_vacancies = Vacancy.objects.filter(specialty__code=specialty).count()
        context = {
            "head_title": head_title,
            "title": title,
            "vacancies": vacancies,
            "number_of_vacancies": number_of_vacancies,
        }

        return render(request, 'vacancies.html', context=context)


class CompanyView(View):

    def get(self, request, company_id):
        head_title = "Компания | "
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return HttpResponseNotFound('Ой, данная страница не найдена((')

        vacancies = Vacancy.objects.filter(company__id=company_id).values('id', 'title', 'skills',
                                                                          'salary_min', 'salary_max', 'published_at')
        number_of_vacancies = Vacancy.objects.filter(company__id=company_id).count()
        context = {
            "head_title": head_title,
            "company": company,
            "vacancies": vacancies,
            "number_of_vacancies": number_of_vacancies,
        }

        return render(request, 'company.html', context=context)


class VacancyView(View):

    def get(self, request, vacancy_id):
        head_title = "Вакансия | "
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return HttpResponseNotFound('Ой, данная страница не найдена((')

        company = Company.objects.get(vacancies__id=vacancy_id)
        context = {
            "head_title": head_title,
            "vacancy": vacancy,
            "company": company,
        }

        return render(request, 'vacancy.html', context=context)


class ApplicationSendView(View):
    def get(self, request):
        return render(request, 'sent.html')


class MyCompanyView(View):
    def get(self, request):
        return render(request, 'company.html')


class MyCompanyVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancy-list.html')


class MyVacancyView(View):
    def get(self, request):
        return render(request, 'vacancy.html')


class LoginView(View):
    def get(self, request):
        return render(request, '.html')


class RegisterView(View):
    def get(self, request):
        return render(request, '.html')


class LogoutView(View):
    def get(self, request):
        return render(request, '.html')
