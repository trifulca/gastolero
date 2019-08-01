from django.db import models

# Create your models here.


class Transaction(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE,
                                related_name='transactions')

    budget = models.ForeignKey(
        'budgets.MonthlyBudget', on_delete=models.CASCADE,
        null=True, blank=True, related_name='transactions'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    pair = models.ForeignKey('self', on_delete=models.SET_NULL,
                             blank=True, null=True)
