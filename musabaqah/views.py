from django.shortcuts import render, redirect
from.forms import LoginUserForm, StateUserForm , CreateUser, EmailLoginForm, ParticipantForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from. models import *
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

def home(request):

    return render(request, "musabaqah/home.html")

def my_login(request):
    form = EmailLoginForm()

    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Try authenticating admin users (User model)
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect("dashboard")
            except User.DoesNotExist:
                pass  # try StateUser next

            # Try authenticating StateUser
            try:
                state_user = StateUser.objects.get(email=email)
                if check_password(password, state_user.password):
                    request.session['state_user_id'] = state_user.id
                    return redirect("state-board")
                else:
                    messages.error(request, "Incorrect password.")
            except StateUser.DoesNotExist:
                messages.error(request, "No user found with that email.")

    return render(request, "musabaqah/my-login.html", {'form': form})


@login_required(login_url="my-login")
def dashboard(request):
    total_users = StateUser.objects.count()
    total_participants = Participant.objects.count()
    context = {'total_users': total_users, 'total_participants':total_participants}
    return render(request, "musabaqah/dashboard.html", context)



def add_admin(request):
    admin = User.objects.filter(is_superuser=True)  
    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password('drammzy123')  
            user.is_superuser = True         
            user.is_staff = True             
            user.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'admin': admin,
    }
    return render(request, 'musabaqah/add-admin.html', context)


@login_required(login_url="my-login")
def state_user(request):
    state = StateUser.objects.all()
    form = StateUserForm()
    if request.method == "POST":
        form = StateUserForm(request.POST, request.FILES)
        if form.is_valid():
            state_user = form.save(commit=False)
            state_user.password = make_password("1234")  # set and hash default password
            state_user.save()
            return redirect("dashboard")
    context = {
        "form": form,
        "state": state
    }
    return render(request, "musabaqah/state-user.html", context)

def participant(request):
    part = Participant.objects.all().order_by('hibz')
    context = {'part':part}
    return render(request, "musabaqah/participants.html",context)

# state users views
def state_board(request):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')

    # Fetch the state user from DB
    state_user = StateUser.objects.get(id=user_id)

    return render(request, 'musabaqah/state-board.html', {'state_user': state_user})


def state_cord(request):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')

    state_user = StateUser.objects.get(id=user_id)
    cord = StateUser.objects.all()
    
    context = {
        'cord': cord,
        'state_user': state_user
    }
    return render(request, 'musabaqah/state-cord.html', context)


def state_part(request):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')

    state_user = StateUser.objects.get(id=user_id)
    
    # Only fetch participants related to this state_user
    part = Participant.objects.filter(state_user=state_user)
    
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.state_user = state_user
            participant.save()
            return redirect('state-board')

    context = {
        'part': part,
        'state_user': state_user,
        'form': form
    }
    return render(request, 'musabaqah/state-part.html', context)




def logout_user(request):
    auth.logout(request)
    return redirect('my-login')
