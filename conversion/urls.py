from django.urls import path
from . import views

urlpatterns = [
    path('<str:original_currency>/<str:destination_currency>/<str:amount>/', views.Conversion.as_view())
]