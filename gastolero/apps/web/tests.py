import datetime
import month

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import Account
from accounts.models import ACCOUNT_CCORRIENTE, ACCOUNT_EFECTIVO
from transactions.models import Transaction
from budgets.models import Budget
from budgets.models import MonthlyBudget


class BasicBudgetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="username")

        self.cuenta_corriente = Account.objects.create(user=self.user,
            kind=ACCOUNT_CCORRIENTE, alias="Banco")

        self.cuenta_efectivo = Account.objects.create(user=self.user,
            kind=ACCOUNT_EFECTIVO, alias="Billetera")

    def test_cuentas_puede_obtener_saldo(self):
        # Inicialmente el balance de las cuentas es 0
        self.assertEqual(self.cuenta_corriente.balance(), 0)
        self.assertEqual(self.cuenta_efectivo.balance(), 0)

        # Si se crea una transacción de ingreso de dinero en la cuenta
        # corriente el balance va a dar positivo.
        self.cuenta_corriente.transactions.create(amount=1000,
            description="Pago de sueldo, $1000",
            timestamp=self.fecha("1/1/2019 10:00"))

        self.assertEqual(self.cuenta_corriente.balance(), 1000)

        # Si se realiza un movimiento de la cuenta corriente a efectivo, por
        # ejemplo si se retira $600 del cajero automático, el saldo
        # sumado de las dos cuentas sigue siendo $1.000, pero $400 en una
        # cuenta y $600 en la otra.

        # FIXME: creo que esto debería hacerse solo, es decir, el sistema
        # debería tener una forma de 'duplicar' estas dos transacciones para
        # que una sume y otra reste
        Transaction.objects.create(account=self.cuenta_corriente, amount=-600,
            description="Extraigo $600 del cajero",
            timestamp=self.fecha("1/1/2019 16:00"))

        Transaction.objects.create(account=self.cuenta_efectivo, amount=600,
            description="Extraigo $600 del cajero y guardo en billetera",
            timestamp=self.fecha("1/1/2019 16:00"))

        self.assertEqual(self.cuenta_corriente.balance(), 400)
        self.assertEqual(self.cuenta_efectivo.balance(), 600)



    def test_puedo_ver_cuanto_falta_presupuestar(self):
        # Actualmenten no hay un modelo que permita acceder a esta
        # información, así que creo que lo mejor es obtenerla a mano,
        # desde los presupuestos. Lo ideal es que exista un modelo
        # tipo "Perfil" que tenga un método que haga esto, el perfil tendría
        # que ser la "raiz" u objeto principal del que cuelgan las cuentas y
        # los presupuestos.

        # Se realiza la prueba con un escenario de cuenta corriente con
        # $1.000 pesos, de los cuales $200 van al presupuesto de supermercado.
        # El resto de dinero sin presupuestar debería ser $800

        # 1 - Se registra el ingreso de $ 1.000 pesos
        self.assertEqual(self.cuenta_corriente.balance(), 0)
        self.cuenta_corriente.transactions.create(amount=1000,
            description="Pago de sueldo, $1000",
            timestamp=self.fecha("1/1/2019 10:00"))
        self.assertEqual(self.cuenta_corriente.balance(), 1000)

        # 2 - Se asignan $200 pesos al prespuesto de supermercado para el
        # mes de Octubre (10)
        presupuesto = Budget.objects.create(user=self.user,
            name="Supermercado",
            description="Compras en supermercado, alimentos, verdulería etc"
        )

        mes_octubre = month.Month(2019, 10)

        presupuesto.create_monthly_budget(mes_octubre)
        supermercado_de_octubre = presupuesto.months.get(month=mes_octubre)

        supermercado_de_octubre.planned = 200
        supermercado_de_octubre.save()


        cuentas = Account.objects.filter(user=self.user)

        ingresos_totales = sum([t.amount for t in Transaction.objects.filter(amount__gt=0)])

        # en YNAB llaman a lo siguiente "Total Budgeted".
        presupuestos_del_mes = MonthlyBudget.objects.filter(month=mes_octubre)
        total_presupuestado = sum([p.planned for p in presupuestos_del_mes])

        # 3 - El dinero sin presupuestar debería ser $800
        self.assertEqual(ingresos_totales - total_presupuestado, 800)


        # Si se hace una compra en el supermercado...
        self.cuenta_corriente.transactions.create(amount=-300,
            description="Compro verduras y tapas de tarta.",
            budget=supermercado_de_octubre,
            timestamp=self.fecha("4/1/2019 15:00"))


        # El dinero sin presupuestar debería ser el mismo.
        self.assertEqual(ingresos_totales - total_presupuestado, 800)

        # El problema es que me pasé en $100 del presupuesto de supermercado
        # (planned era 200, gasté 300, debería quedarme available=-100)
        self.assertEqual(supermercado_de_octubre.balance(), -100)

        # Si arreglo el presupuesto de supermercado, para que cierre:
        supermercado_de_octubre.planned = 300
        supermercado_de_octubre.save()

        # Ahora si, el balance (available) debería dar 0
        self.assertEqual(supermercado_de_octubre.balance(), 0)

        # pero, mi "to be budget" debería dar 700
        ingresos_totales = sum([t.amount for t in Transaction.objects.filter(amount__gt=0)])
        presupuestos_del_mes = MonthlyBudget.objects.filter(month=mes_octubre)
        total_presupuestado = sum([p.planned for p in presupuestos_del_mes])
        self.assertEqual(ingresos_totales - total_presupuestado, 700)



    def fecha(self, cadena):
        d = datetime.datetime.strptime(cadena, "%d/%m/%Y %H:%M")
        current_tz = timezone.get_current_timezone()
        return current_tz.localize(d)
