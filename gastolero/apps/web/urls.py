from django.urls import path
from .views import status, account_move, TransactionListView

app_name = 'web'
urlpatterns = [
    path('status/', status, name='status'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('account/move/', account_move),
]
