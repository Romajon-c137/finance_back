from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from .models import *


@receiver(post_save, sender=Consumption)
def note_post_save(sender, instance: Consumption, created, **kwargs):
    if created:
        person = instance.person

        Person.objects.filter(pk=person.pk).update(
            total_sum=F("total_sum") + instance.cash
        )


@receiver(post_save, sender=Salary)
def note_post_save(sender, instance: Consumption, created, **kwargs):
    if created:
        person = instance.person

        Person.objects.filter(pk=person.pk).update(
            total_sum=F("total_sum") + instance.cash
        )


# Finance
@receiver(post_save, sender=Finance)
def note_post_save(sender, instance: Finance, created, **kwargs):
    if created:
        person = instance.person
        type_finance = instance.type_finance

        if type_finance == CHOICES_TYPE_FINANCE[1][0]:
            Person.objects.filter(pk=person.pk).update(
                total_sum=F("total_sum") + instance.cash
            )
        else:
            Person.objects.filter(pk=person.pk).update(
                total_sum=F("total_sum") - instance.cash
            )
