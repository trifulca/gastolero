import month
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from transactions.models import Transaction
from accounts.models import Account
from budgets.models import MonthlyBudget
from .forms import AssignmentForm, SpendForm


def current_month():
    a = datetime.utcnow()
    return month.Month(a.year, a.month)


@login_required
def status(request):
    # cur_month = current_month()
    cur_month = month.Month(2019, 8)

    # accounts = Account.objects.filter(user=request.user)
    accounts = Account.objects.filter(user_id=2)
    accounts_total = sum([a.balance() for a in accounts])

    budgets = MonthlyBudget.objects.filter(month=cur_month)

    la_guita = Transaction.objects.filter(budget__isnull=True).aggregate(t=Sum('amount'))['t']
    budgets_total = MonthlyBudget.objects.filter(budget__user_id=2).aggregate(t=Sum('planned'))['t']
    unbadgeted = la_guita - budgets_total

    return render(request, 'web/status.html', {
        'accounts': accounts,
        'accounts_total': accounts_total,
        'budgets': budgets,
        'unbudgeted': unbadgeted,
    })


def spend_add(request):
    form = SpendForm()

    return render(request, 'web/spend_add.html', {
        'form': form
    })


def assignment_add(request):
    form = AssignmentForm()

    return render(request, 'web/spend_add.html', {
        'form': form
    })
