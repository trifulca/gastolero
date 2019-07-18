from django.contrib import admin

from .models import Budget, MonthlyBudget

# Register your models here.


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('budget', 'month', 'planned')
