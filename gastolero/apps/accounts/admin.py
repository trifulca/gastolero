from django.contrib import admin

# Register your models here.


from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'kind', 'alias', 'entity', 'cbu_cvu',
                    'external_id')
