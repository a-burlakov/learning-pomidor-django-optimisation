from django.core.validators import MaxValueValidator
from django.db import models
from readline import set_completion_display_matches_hook

from clients.models import Client
from services.tasks import set_comment


class Service(models.Model):
    """
    Сервис.
    """

    name = models.CharField("Наименование", max_length=255)
    full_price = models.PositiveIntegerField("Цена")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, save_model=True, **kwargs):
        from services.tasks import set_price

        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)

        return super().save(*args, **kwargs)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, save_model=True, **kwargs):
        from services.tasks import set_price

        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)

        return super().save(*args, **kwargs)


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
    price = models.PositiveIntegerField("Цена", default=0)
    comment = models.CharField("Комментарий", max_length=255)
