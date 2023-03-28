from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name="Клиент")
    company_name = models.CharField("Компания", max_length=255)
    full_address = models.CharField("Адрес", max_length=1024)
