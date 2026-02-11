from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Consumption, Person, Finance, Salary


@admin.register(Finance)
class FinanceAdmin(ModelAdmin):

    list_display = (
        "id",
        "name",
        "cash",
        "type_finance",
        "return_cash",
    )

    list_display_links = list_display


@admin.register(Person)
class PersonAdmin(ModelAdmin):

    list_display = (
        "id",
        "name",
        "total_sum",
        "content_type",
    )

    list_display_links = list_display

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "total_sum",
                    "content_type",
                    "owner",
                ),
            },
        ),
    )


@admin.register(Consumption)
class ConsumptionAdmin(ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    list_display_links = list_display


@admin.register(Salary)
class SalaryAdmin(ModelAdmin):

    list_display = (
        "id",
        "cash",
    )

    list_display_links = list_display
