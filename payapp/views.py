import decimal
from django.shortcuts import render , redirect, get_object_or_404
from payapp.forms import SentPayment, RequestPayment
from django.template.loader import render_to_string
from .models import Balance
from .models import Notification, Transaction
from django.db import transaction, OperationalError
from django.db.models import F, Q
from . import models
from django.http import Http404, HttpResponse
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required





def payapp(request):
    raise Http404()


@login_required
def home(request):
    userbalance = models.Balance.objects.select_related().get(name=request.user)
    return render(request, "payapp/home.html", {'userbalance': userbalance})


@login_required
def reject_request(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    if request.method == "POST":
        notification.delete()
        notifications = Notification.objects.filter(requested_from=request.user)
        return redirect('/payapp/viewNotifications', {"notification_list": notifications})
    return render(request, 'payapp/reject_request.html', {'notification': notification})


@login_required
def accept_request(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    if request.method == 'POST':
        sender = notification.requested_from
        receiver = notification.requested_by
        amount = notification.amount
        sender_balance = models.Balance.objects.select_related().get(name__username=sender)
        receiver_balance = models.Balance.objects.select_related().get(name__username=receiver)
        amount_to_receive = convert_currency(sender_balance.currency, receiver_balance.currency, amount)
        new_transaction = Transaction.objects.create(sender = sender, receiver=receiver, amount=amount)
        try:
            with transaction.atomic():
                sender_balance.balance = sender_balance.balance - amount
                sender_balance.save()
                receiver_balance.balance = receiver_balance.balance + decimal.Decimal(amount_to_receive)
                receiver_balance.save()
                new_transaction.save()
                notification.delete()
        except OperationalError:
            messages.info(request, f"Transaction failed")
        return render(request, "payapp/sent_success.html", {"sender": sender_balance, "receiver_name": receiver_balance.name, "amount": amount})
    return render(request, "payapp/accept_request.html", {'notification': notification})


@login_required
def requestPayment(request):
    if request.method == 'POST':
        form = RequestPayment(request.POST)
        if form.is_valid():
            requested_from = form.cleaned_data["requested_from"]
            if not Balance.objects.filter(name__username=requested_from).exists():
                messages.info(request, "This user does not exists")
                return redirect('requestPayment')
            amount = form.cleaned_data["amount"]
            new_request = Notification.objects.create(requested_by=request.user.username, requested_from=requested_from, amount=amount)
            new_request.save()
            return render(request, "payapp/request_success.html", {"receiver_name": requested_from, "amount": amount})
    else:
        form = RequestPayment()
        return render(request, "payapp/request_payment.html", {"form": form})


@login_required()
def sent_payment(request):
    if request.method == 'POST':
        form = SentPayment(request.POST)

        if form.is_valid():
            sender = request.user.username
            receiver = form.cleaned_data["receiver"]
            amount = form.cleaned_data["amount"]

            if not Balance.objects.filter(name__username=receiver).exists():
                messages.info(request, "This user does not exists")
                return redirect('sentPayment')

            sender_balance = Balance.objects.select_related().get(name__username=sender)
            receiver_balance = Balance.objects.select_related().get(name__username=receiver)
            amount_to_receive = convert_currency(sender_balance.currency, receiver_balance.currency, amount)
            new_transaction = Transaction.objects.create(sender = sender, receiver=receiver, amount=amount)

            try:
                with transaction.atomic():
                    sender_balance.balance = sender_balance.balance - amount
                    sender_balance.save()

                    receiver_balance.balance = receiver_balance.balance + decimal.Decimal(amount_to_receive)
                    receiver_balance.save()

                    new_transaction.save()
            except OperationalError:
                messages.info(request, f"Transaction failed")

            return render(request, "payapp/sent_success.html", {"sender": sender_balance, "receiver_name": receiver_balance.name, "amount": amount})

        else:
            messages.info(request, "The payment could not be sent, please try again!")

    else:
        form = SentPayment()
        return render(request, "payapp/sent_payment.html", {"form": form})

def sent_success(request):
    return render(request, "payapp/sent_success.html")


def viewNotifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(requested_from=request.user)
        return render(request, "payapp/view_notifications.html", {"notification_list": notifications})

    else:
        return render(request, "payapp/view_transactions.html")


def viewTransactions(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        return render(request, "payapp/view_transactions.html", {"transaction_list": transactions})

    else:
        return render(request, "payapp/view_transactions.html")


def convert_currency(currency1, currency2, amount):
    if currency1 == currency2:
        return amount
    else:
        url = "http://localhost:8000/conversion/{}/{}/{}".format(currency1, currency2, amount)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["destination_amount"]
