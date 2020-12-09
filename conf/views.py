from django.db.models import Count
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from jobs.models import Specialty, Company


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, данная страница не найдена((')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что-то стряслось с сервером... Скоро все починим')


class MainView(View):

    def get(self, request):
        head_title = ""
        specialties = Specialty.objects.all().annotate(Count('vacancies'))
        companies = Company.objects.all().annotate(Count('vacancies'))

        context = {
            "head_title": head_title,
            "specialties": specialties,
            "companies": companies,
        }

        return render(request, 'index.html', context=context)
