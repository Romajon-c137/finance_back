from django.db import models
from utils.models import DataTimeCUAbstract, BaseFinance, Base
from core.constants import CHOICES_TYPE_FINANCE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Finance(BaseFinance):
    """Модель для финанс"""

    type_finance = models.CharField(
        "Тип операции",
        max_length=5,
        choices=CHOICES_TYPE_FINANCE,
    )
    return_cash = models.BooleanField(
        "Возврат денег",
        default=False,
    )

    class Meta:
        verbose_name = "Финанс"
        verbose_name_plural = "Финансы"

    def __str__(self):
        return f"{self.pk}) {self.name}"


class Person(Base):
    """Модель для персона"""

    owner = models.ForeignKey(
        "account.User",
        models.CASCADE,
        related_name="persons",
        verbose_name="Владелиц",
    )
    total_sum = models.DecimalField(
        "Общая сумма",
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Тип объекта",
    )
    object_id = models.PositiveIntegerField("ID объекта", null=True, blank=True)
    type_ope = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"


class Consumption(BaseFinance):
    """Модель для расход"""

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"


class Salary(BaseFinance):
    """Модель для зарплаты"""

    name = None

    class Meta:
        verbose_name = "Зарплата"
        verbose_name_plural = "Зарплаты"


CLASS_TYPE_FINANCE_CHOICES_MAPPING = {
    "finance": Finance,
    "consumption": Consumption,
    "salary": Salary,
}
