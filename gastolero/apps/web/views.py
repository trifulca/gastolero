from django.shortcuts import render

from accounts.models import Account
from budgets.models import MonthlyBudget


def status(request):
    accounts = Account.objects.all()
    budgets = MonthlyBudget.objects.filter(month='2019-07')

    return render(request, 'web/status.html', {
        'accounts': accounts,
        'budgets': budgets,
    })
