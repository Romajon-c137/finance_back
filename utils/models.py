from django.db import models
from core.constants import CHOICES_TYPE_FINANCE


class DataTimeCUAbstract(models.Model):
    create_dt = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    update_dt = models.DateTimeField(
        "Дата обновления",
        auto_now=True,
    )

    class Meta:
        abstract = True


class Base(DataTimeCUAbstract):
    name = models.CharField(
        "Названия",
        max_length=65,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk}) {self.name}"


class BaseFinance(Base):
    owner = models.ForeignKey(
        "account.User",
        models.CASCADE,
        verbose_name="Владелиц",
    )
    cash = models.DecimalField(
        "Сумма",
        max_digits=10,
        decimal_places=2,
    )
    person = models.ForeignKey(
        "Person",
        models.CASCADE,
    )

    class Meta:
        abstract = True
