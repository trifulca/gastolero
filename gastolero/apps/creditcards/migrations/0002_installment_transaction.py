# Generated by Django 2.2.3 on 2023-07-22 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creditcards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timestamp', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creditcards.CreditCard')),
                ('installments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='creditcards.Installment')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
