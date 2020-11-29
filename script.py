import os
import django
from django.db.models import Value
from django.db.models.functions import Replace

from jobs.data import companies, specialties, jobs

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

from jobs.models import Vacancy, Company, Specialty

if __name__ == '__main__':
    for company in companies:
        Company.objects.create(
            name=company['title'],
            location=company['location'],
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for specialty in specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for job in jobs:
        Vacancy.objects.create(
            title=job['title'],
            company=Company.objects.get(id=job['company']),
            specialty=Specialty.objects.get(code=job['specialty']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )

    Vacancy.objects.update(skills=Replace('skills', Value(', '), Value(' • ')))
