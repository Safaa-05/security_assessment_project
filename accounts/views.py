from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


# Home Page
def home(request):
    return render(request, "accounts/home.html")


# Register
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# Login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                form.add_error(None, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


# Logout
def user_logout(request):
    logout(request)
    return redirect("login")


# Dashboard
@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")