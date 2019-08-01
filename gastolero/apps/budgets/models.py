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

    def create_monthly_budget(self, month):
        qs_check = self.months.filter(month=month)
        if qs_check.count() == 1:
            return qs_check.first()

        return MonthlyBudget.objects.create(budget=self, month=month,
                                            planned=0)


class MonthlyBudget(models.Model):
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE,
                               related_name='months')
    month = MonthField()
    planned = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('budget', 'month')
        ordering = ('month', 'budget__name')

    def __str__(self):
        return '{} ({})'.format(self.budget, self.month._date.strftime('%B'))

    def balance(self):
        return self.planned + \
               self.transactions.aggregate(s=Coalesce(Sum('amount'), 0))['s']
