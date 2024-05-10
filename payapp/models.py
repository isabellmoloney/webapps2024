from django.db import models
from django.contrib.auth.models import User


CURRENCY_CHOICES = (
    ("GBP", "British pounds"),
    ("EUR", "Euro"),
    ("USD", "US Dollar"),
)


# Create your models here.
class Transaction(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    def __str__(self):
        details = ''
        details += f'Sender   : {self.sender}\n'
        details += f'Receiver : {self.receiver}\n'
        details += f'Amount   : {self.amount}\n'
        details += f'sent in: {self.currency}\n'
        return details


class Balance(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=1000.00, decimal_places=2, max_digits=8)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)

    def __str__(self):
        details = ''
        details += f'name    : {self.name}\n'
        details += f'balance : {self.balance}\n'
        details += f'currency: {self.currency}\n'
        return details


class Notification(models.Model):
    requested_by = models.CharField(max_length=100)
    requested_from = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        details = ''
        details += f'from   : {self.requested_from}\n'
        details += f'to     : {self.requested_by}\n'
        details += f'amount : {self.amount}\n'
        return details




class ConversionResponse(models.Model):
    conversion_rate = models.DecimalField(decimal_places=2, max_digits=8)
    destination_amount = models.DecimalField(decimal_places=2, max_digits=8)

