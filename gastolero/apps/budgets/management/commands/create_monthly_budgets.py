import month
from django.core.management.base import BaseCommand

from budgets.models import Budget


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Example: 2019')
        parser.add_argument('month', type=int, help='Example: 12')

    def handle(self, *args, **options):
        the_month = month.Month(options['year'], options['month'])

        for budget in Budget.objects.all():
            budget.create_monthly_budget(the_month)
