from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

from month.models import MonthField

# Create your models here.


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class MonthlyBudget(models.Model):
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE)
    month = MonthField()
    planned = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return '{} - {}'.format(self.budget, self.month)

    def balance(self):
        return self.planned + \
               self.transactions.aggregate(s=Coalesce(Sum('amount'), 0))['s']
