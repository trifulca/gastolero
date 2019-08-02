from django.urls import path
from .views import status, account_add, account_move

app_name = 'web'
urlpatterns = [
    path('status/', status, name='status'),
    path('account/add/', account_add),
    path('account/move/', account_move),
]
