import month
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum
from django.db import transaction

from transactions.models import Transaction
from accounts.models import Account
from budgets.models import MonthlyBudget
from .forms import SpendForm, AccountMoveForm


def current_month():
    a = datetime.utcnow()
    return month.Month(a.year, a.month)


@login_required
def status(request):
    # cur_month = current_month()
    cur_month = month.Month(2019, 8)

    accounts = Account.objects.filter(user=request.user)
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


def account_add(request):
    form = SpendForm()

    return render(request, 'web/spend_add.html', {
        'form': form
    })


def account_move(request):

    if request.method == 'POST':
        form = AccountMoveForm(user=request.user, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                ts = Transaction.objects.create(
                    account=form.cleaned_data['source'],
                    amount=form.cleaned_data['amount'] * -1,
                    timestamp='2019-01-01 01:01:01'
                )

                tt = Transaction.objects.create(
                    account=form.cleaned_data['target'],
                    amount=form.cleaned_data['amount'],
                    timestamp='2019-01-01 01:01:01',
                    pair=ts
                )
                ts.pair = tt
                ts.save()

            return redirect(reverse('web:status'))

    else:
        form = AccountMoveForm(user=request.user)

    return render(request, 'web/account_move.html', {
        'form': form
    })
