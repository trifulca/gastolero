# Generated by Django 2.2.3 on 2019-08-01 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import month.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', month.models.MonthField()),
                ('planned', models.DecimalField(decimal_places=2, max_digits=12)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='budgets.Budget')),
            ],
            options={
                'ordering': ('month', 'budget__name'),
                'unique_together': {('budget', 'month')},
            },
        ),
    ]
