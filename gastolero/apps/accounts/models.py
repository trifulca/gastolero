from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

# Create your models here.

# TODO: Pasar esto a un archivo externo cuando esté maomeno definido
ACCOUNT_CAHORRO = 'ahorro'
ACCOUNT_CCORRIENTE = 'corriente'
ACCOUNT_EFECTIVO = 'efete'
ACCOUNT_DIGITAL = 'digital'
ACCOUNT_PLAZO = 'plazo'

ACCOUNT_CHOICES = (
    (ACCOUNT_CAHORRO, 'Caja de Ahorro'),
    (ACCOUNT_CCORRIENTE, 'Cuenta Coriente'),
    (ACCOUNT_EFECTIVO, 'Efectivo'),
    (ACCOUNT_DIGITAL, 'Billetera digital'),
    (ACCOUNT_PLAZO, 'Plazo fijo'),
)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    kind = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    alias = models.CharField(max_length=30)

    entity = models.CharField(max_length=30, null=True, blank=True)
    cbu_cvu = models.PositiveIntegerField(verbose_name='CBU/CVU',
                                          null=True, blank=True)
    external_id = models.CharField(max_length=300, null=True, blank=True)

    # tipo (caja de ahorro, cuenta corriente, plazo fijo, coso virtual, fci)
    # entidad
    # nickname
    # cbu/cvu ¿?

    class Meta:
        ordering = ['alias']

    def __str__(self):
        return '{}'.format(self.alias)

    def balance(self):
        return self.transactions.aggregate(s=Coalesce(Sum('amount'), 0))['s']
