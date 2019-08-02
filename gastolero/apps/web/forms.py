from django import forms

from transactions.models import Transaction
from accounts.models import Account


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account', 'timestamp', 'amount',
                  'description')


class SpendForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account', 'budget', 'timestamp', 'amount', 'description')


class AccountMoveForm(forms.Form):
    source = forms.ModelChoiceField(queryset=None,
                                    to_field_name='alias')
    target = forms.ModelChoiceField(queryset=None,
                                    to_field_name='alias')
    amount = forms.DecimalField()

    def __init__(self, user, *args, **kwargs):
        super(AccountMoveForm, self).__init__(*args, **kwargs)

        self.fields['source'].queryset = Account.objects.filter(user=user)
        self.fields['target'].queryset = Account.objects.filter(user=user)
