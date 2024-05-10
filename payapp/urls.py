from django.urls import path
from . import views

urlpatterns = [
    path('', views.payapp, name='payapp'),
    path('home/', views.home, name='home'),
    path('sentPayment/', views.sent_payment, name='sentPayment'),
    path('requestPayment/', views.requestPayment, name='requestPayment'),
    path('viewTransactions/', views.viewTransactions, name='viewTransactions'),
    path('viewNotifications/', views.viewNotifications, name='viewNotifications'),
    path('sentsuccess/', views.sent_success, name='sentsuccess'),
    path('rejectrequest/<int:notification_id>/', views.reject_request, name='rejectrequest'),
    path('acceptrequest/<int:notification_id>/', views.accept_request, name='acceptrequest')
]
