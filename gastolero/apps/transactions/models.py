from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Transaction(models.Model):
    source = models.ForeignKey('accounts.Account', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='transactions')
    destination = models.ForeignKey('accounts.Account',
                                    on_delete=models.CASCADE,
                                    null=True, blank=True)
    budget = models.ForeignKey(
        'budgets.Budget', on_delete=models.CASCADE,
        null=True, blank=True
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
