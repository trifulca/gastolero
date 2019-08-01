from django import forms

from transactions.models import Transaction


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account', 'timestamp', 'amount',
                  'description')


class SpendForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account', 'budget', 'timestamp', 'amount', 'description')
