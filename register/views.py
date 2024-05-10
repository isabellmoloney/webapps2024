from django.shortcuts import render

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

from django.shortcuts import render, redirect
from register.forms import RegisterForm
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "payapp/home.html")
        else:
            messages.info(request, "Registration failed, please try again")
            return redirect('register')
    else:
        return render(request, "register/register.html", {'register_user': RegisterForm})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/payapp/home/')
            else:
                messages.info(request, "Login failed, please try again")
            return redirect('login')
        else:
            messages.info(request, "Login failed, please try again")
            return redirect('login')
    else:
        return render(request, "register/login.html", {'login_user': AuthenticationForm})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


