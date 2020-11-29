from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=120)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()

    def __str__(self):
        return f'id={self.pk}, name={self.name}, location={self.location}, employee_count={self.employee_count}'


class Specialty(models.Model):
    code = models.CharField(max_length=120, unique=True)
    title = models.CharField(max_length=120)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return f'id={self.pk}, code={self.code}, title={self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return f'id={self.pk}, title={self.title}, specialty={self.specialty}, company={self.company}, ' \
               f'salary_min={self.salary_min}, salary_max={self.salary_max}'
