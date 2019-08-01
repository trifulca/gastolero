from django.urls import path
from .views import status, spend_add, assignment_add

urlpatterns = [
    path('status/', status),
    path('spend/add/', spend_add),
    path('assignment/add/', assignment_add),
]
