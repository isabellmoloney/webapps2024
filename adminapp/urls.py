from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('view-all-transactions/', views.view_all_transactions, name="alltransactions"),
    path('view-balances/', views.view_balances, name="allbalances")
]