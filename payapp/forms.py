from django import forms
from . import models


class SentPayment(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ["receiver", "amount"]


class RequestPayment(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["requested_from", "amount"]