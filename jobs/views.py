from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from django.views import View

from jobs.forms import RegistrationForm, ApplicationForm, CompanyForm, VacancyForm
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
            "form": ApplicationForm,
        }

        return render(request, 'vacancy.html', context=context)

    def post(self, request, vacancy_id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy_id = vacancy_id
            application.save()
            return redirect(f'{vacancy_id}/send', {'vacancy_id': vacancy_id})
        return render(request, request.path, {'form': form})


class ApplicationSendView(View):
    def get(self, request, vacancy_id):
        return render(request, 'sent.html', {'vacancy_id': vacancy_id})

    # Отклик отправлен


class MyCompanyView(View):
    def get(self, request):
        head_title = "Моя компания | "
        try:
            company = Company.objects.get(owner=request.user.id)
        except Company.DoesNotExist:
            return redirect('lets_start')

        context = {
            "head_title": head_title,
            "company": company,
            'form': CompanyForm(instance=company),
        }

        return render(request, 'mycompany.html', context=context)

    def post(self, request):
        company = Company.objects.get(owner=request.user.id)
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        return render(request, 'mycompany.html', {'form': form})


class LetsStartView(View):
    def get(self, request):
        return render(request, 'company-lets_start.html')


class MyCompanyCreateView(View):
    def get(self, request):
        head_title = "Моя компания | "
        return render(request, 'company-create.html', {'head_title': head_title, 'form': CompanyForm()})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('/mycompany.html')
        return render(request, 'company-create.html', {'form': form})


class MyCompanyVacanciesView(View):
    def get(self, request):
        head_title = "Мои вакансии | "
        try:
            company = Company.objects.get(owner=request.user.id)
        except Specialty.DoesNotExist:
            return redirect('lets_start')

        vacancies = Vacancy.objects.filter(company_id=company.id).values('id', 'title', 'salary_min', 'salary_max')
        context = {
            "head_title": head_title,
            "vacancies": vacancies,
        }

        return render(request, 'vacancy-list.html', context=context)


class MyVacancyView(View):
    def get(self, request, vacancy_id):
        head_title = "Моя вакансия | "
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return redirect('my_vacancy_create')

        context = {
            "head_title": head_title,
            "vacancy": vacancy,
            'form': VacancyForm(instance=vacancy),
        }

        return render(request, 'vacancy-edit.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = VacancyForm(request.POST, request.FILES, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        return render(request, 'vacancy-edit.html', {'form': form})


class MyVacancyCreateView(View):
    def get(self, request):
        head_title = "Моя вакансия | "
        return render(request, 'vacancy-edit.html', {'head_title': head_title, 'form': VacancyForm()})

    def post(self, request):
        form = VacancyForm(request.POST, request.FILES)
        company = Company.objects.get(owner_id=request.user.id)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company_id = company.id
            vacancy.save()
            return redirect(f'/mycompany/vacancies/{vacancy.id}')
        return render(request, 'vacancy-edit.html', {'form': form})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html', {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан')
            return redirect('login')
        return render(request, 'register.html', {'form': form})
