from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


class Service(models.Model):
    """
    Сервис.
    """

    name = models.CharField("Наименование", max_length=255)
    full_price = models.PositiveIntegerField("Цена")


class Plan(models.Model):
    """
    План подписки.
    """

    PLAN_TYPES = (
        ("full", "Full"),
        ("student", "Student"),
        ("discount", "Discount"),
    )

    plan_type = models.CharField("Тип плана", choices=PLAN_TYPES, max_length=255)
    discount_percent = models.PositiveIntegerField(
        "Процент скидки",
        default=0,
        validators=[
            MaxValueValidator(100),
        ],
    )

    def __str__(self):
        return f"{self.plan_type} (disc. {self.discount_percent}%)"


class Subscription(models.Model):
    """
    Подписки клиентов на сервис.
    """

    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        related_name="subscriptions",
        on_delete=models.PROTECT,
    )
    service = models.ForeignKey(
        Service,
        verbose_name="Сервис",
        related_name="subscriptions",
        on_delete=models.PROTECT,
    )
    plan = models.ForeignKey(
        Plan,
        verbose_name="Тарифный план",
        related_name="subscriptions",
        on_delete=models.PROTECT,
    )
