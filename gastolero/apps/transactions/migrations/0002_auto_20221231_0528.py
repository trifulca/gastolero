# Generated by Django 2.2.3 on 2022-12-31 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-timestamp',)},
        ),
    ]
