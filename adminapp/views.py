from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from payapp.models import Balance, Transaction
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

def home(request):
    if not request.user.has_perm('auth.view_user'):
        raise PermissionDenied()
    return render(request, 'adminapp/admin_home.html')


@login_required()
def view_all_transactions(request):
    if not request.user.has_perm('auth.view_user'):
        raise PermissionDenied()
    transactions = Transaction.objects.all()
    return render(request, 'adminapp/view_all_transactions.html', {"transaction_list": transactions})


def view_balances(request):
    if not request.user.has_perm('auth.view_user'):
        raise PermissionDenied()
    balances = Balance.objects.all()
    return render(request, 'adminapp/view_balances.html', {"balance_list": balances})


def admin_console(request):
    if not request.user.has_perm('auth.view_user'):
        raise PermissionDenied()
    return redirect('admin')


