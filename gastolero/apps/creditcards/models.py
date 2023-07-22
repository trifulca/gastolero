from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    alias = models.CharField(max_length=30)
    entity = models.CharField(max_length=30, null=True, blank=True)
    ending = models.CharField(max_length=4, null=True, blank=True)
    external_id = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ['alias']

    def __str__(self):
        return '{} ...{}'.format(self.alias, self.ending)

    def balance(self):
        return self.transactions.aggregate(s=Coalesce(Sum('amount'), 0))['s']


class Transaction(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    installment = models.ForeignKey('Installment', on_delete=models.CASCADE,
                                    null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-timestamp', )

    def __str__(self):
        return '{} {} {}'.format(self.timestamp, self.amount, self.description)


class Installment(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    @staticmethod
    def create_transactions(installment):
        amount = installment.amount / Decimal(installment.quantity)

        for i in range(installment.quantity):
            timestamp = installment.timestamp + relativedelta(months=i)

            Transaction.objects.create(
                card=installment.card,
                installment=installment,
                amount=amount,
                timestamp=timestamp,
                description=installment.description,
            )
