from django.shortcuts import render, redirect
from.forms import LoginUserForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "musabaqah/home.html")

def my_login(request):
    form = LoginUserForm()
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user) 
                return redirect("dashboard")   

    context = {'form':form}
    return render(request, "musabaqah/my-login.html", context)


@login_required(login_url="my-login")
def dashboard(request):
    return render(request, "musabaqah/dashboard.html")

@login_required(login_url="my-login")
def state_user(request):
    return render(request, "musabaqah/state-user.html")

def participant(request):
    return render(request, "musabaqah/participants.html")

def logout_user(request):
    auth.logout(request)
    return redirect('my-login')
