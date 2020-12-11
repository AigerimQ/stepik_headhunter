from django.db import models
from django.contrib.auth import get_user_model

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=120)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(get_user_model(), on_delete=models.PROTECT,
                                 related_name='company')

    def __str__(self):
        return f'id={self.pk}, name={self.name}, location={self.location}, employee_count={self.employee_count}'


class Specialty(models.Model):
    code = models.CharField(max_length=120, unique=True)
    title = models.CharField(max_length=120)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

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
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'id={self.pk}, title={self.title}, specialty={self.specialty}, company={self.company}, ' \
               f'salary_min={self.salary_min}, salary_max={self.salary_max}'


class Application(models.Model):
    written_username = models.CharField(max_length=120)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f'id={self.pk}, written_username={self.written_username}, written_phone={self.written_phone}, ' \
               f'written_cover_letter={self.written_cover_letter},'
