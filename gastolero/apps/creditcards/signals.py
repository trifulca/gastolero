from django.db.models.signals import post_save
from django.dispatch import receiver

from creditcards.models import (
    Installment,
    Transaction,
)


@receiver(post_save, sender=Installment)
def create_transactions(sender, instance, created, **kwargs):
    if created:
        Installment.create_transactions(instance)

    else:
        Transaction.objects.filter(installment__pk=instance.pk).delete()
        Installment.create_transactions(instance)
