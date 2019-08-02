from django.urls import path
from .views import status, account_add, account_move

urlpatterns = [
    path('status/', status),
    path('account/add/', account_add),
    path('account/move/', account_move),
]
