from django.contrib import admin

from creditcards.models import CreditCard, Transaction, Installment


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'alias', 'entity', 'ending', 'external_id')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('card', 'amount', 'timestamp', 'description')


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'timestamp', 'description', 'quantity')
