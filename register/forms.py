from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from payapp.models import Balance, CURRENCY_CHOICES
import requests



class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "currency"]

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        Balance.objects.create(name=instance, balance=convert_intial(self.cleaned_data["currency"]), currency=self.cleaned_data["currency"])
        return instance


def convert_intial(destination):
    if destination == "GBP":
        return 1000
    else:
        url = "http://localhost:8000/conversion/GBP/{}/1000".format(destination)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["destination_amount"]



