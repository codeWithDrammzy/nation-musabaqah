from django.shortcuts import render, redirect
from django.urls import reverse
from.forms import * 
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from. models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import string
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from .models import Post, Participant, StateUser  # adjust model names as needed

def home(request):
    q = request.GET.get('q', '').strip()

    if q:
        # Filter participants instead of using get()
        participants = Participant.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

        if participants.exists():
            participant = participants.first()

            # Try to find the state for this participant
            state_user = StateUser.objects.filter(participant=participant).first()

            if state_user:
                return redirect('registered-state', state=state_user.state)
            else:
                messages.error(request, "This participant has no registered state.")
        else:
            messages.error(request, "Participant not found.")

    # Normal page load
    posts = Post.objects.all().order_by('-created_at')

    unique_states = {}
    for user in StateUser.objects.all():
        unique_states[user.state] = user  # one per state
    state_list = unique_states.values()

    context = {
        'posts': posts,
        'states': state_list,
    }

    return render(request, 'musabaqah/home.html', context)

def about(request):
    return render(request, 'musabaqah/about.html')

def registered_state_view(request, state):
    participants = Participant.objects.filter(stateuser__state=state)
    state_user = StateUser.objects.filter(state=state).first()

    context = {
        'state': state_user,
        'participants': participants,
    }
    return render(request, 'musabaqah/registered_state.html', context)

def registered_state(request, state_code):
    state_users = StateUser.objects.filter(state=state_code)
    participants = Participant.objects.filter(state_user__state=state_code).order_by('hibz')

    unique_states = {}
    for user in StateUser.objects.all():
        unique_states[user.state] = user  # Keeps one user per state

    states = unique_states.values()

    context = {
        'state_users': state_users,
        'participants': participants,
        'state_code': state_code,
        'states': states  # ✅ Renamed to 'states' for clarity in template
    }

    return render(request, 'musabaqah/registered-state.html', context)

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
            messages.success(request, 'Coordinator registered successfully.')
            return redirect("state-user")
        else:
            messages.error(request, 'State Coordinator Alrady exist.')
            return redirect("state-user")
        
        

    context = {
        "form": form,
        "state": state
    }
    return render(request, "musabaqah/state-user.html", context)

@login_required(login_url="my-login")
def participant(request):
    part = Participant.objects.all().order_by('hibz')
    context = {'part':part}
    return render(request, "musabaqah/participants.html",context)

@login_required(login_url="my-login")
def state_user_view(request, pk):
    try:
        state_user = StateUser.objects.get(id=pk)
        part = Participant.objects.filter(state_user=state_user).order_by('hibz')

    except StateUser.DoesNotExist:
        messages.error(request, "State user not found.")
        return redirect("state-user")

    context = {
        'state_user': state_user,
        'part': part
    }
    return render(request, 'musabaqah/state-user-view.html', context)

@login_required(login_url='my-login')
def state_user_delete(request, pk):
    state_user = StateUser.objects.get(id=pk)
    if request.method == 'POST':
        state_user.delete()
        return redirect('state-user')
    context = {'state_user':state_user}
    return render(request, 'musabaqah/dashboard.html', context)

@login_required(login_url='my-login')

def post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            messages.success(request, "Post added successfully")
            return redirect(reverse('post')+'#add-post')
        else:
            messages.error(request, 'Failed to add this post')
            return redirect('post')

       
    posts = Post.objects.all().order_by('-created_at')  # Fetch all posts
    participants = Participant.objects.select_related('state_user').all()

    return render(request, 'musabaqah/post.html', {
        'form': form,
        'posts': posts,  # 👈 Add this
        'part': participants,
    })


def post_detail(request, pk):
    post =get_object_or_404(Post, pk=pk)
    all_states = StateUser.objects.all()
    unique_states = {}
    for user in all_states:
        unique_states[user.state] = user  # use the last user for each state
    states = unique_states.values()  # now you have distinct model instances

    return render(request, 'musabaqah/post-detail.html', {'post': post, 'states':states})


@login_required(login_url="my-login")
def post_view(request, pk):  
    post = get_object_or_404(Post, id=pk)
    context = {'post': post}
    return render(request, "musabaqah/post-view.html", context)

@login_required(login_url="my-login")
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'You Updated This Post!')
            return redirect('post-view', pk=post.pk)  

    return render(request, "musabaqah/post-edit.html", {"form": form, "post": post})

@login_required(login_url='my-login')

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('post')  

    return render(request, 'musabaqah/post_confirm_delete.html', {'post': post})


# state users views
def state_board(request):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')

    # Fetch the state user from DB
    state_user = StateUser.objects.get(id=user_id)
    participants = Participant.objects.all().order_by('state_user')
    part_total = Participant.objects.count()
    state_total = StateUser.objects.count()

    context = {'state_user': state_user,
               'participants': participants,
                'part_total': part_total,
                'state_total':state_total
                
    }
    return render(request, 'musabaqah/state-board.html', context)

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
            messages.success(request, 'Participant registered successfully.')

            return redirect(reverse('state-part') + '#add-participant-form')
        else:
            messages.error(request, ' category already exists.')
            return redirect(reverse('state-part') + '#add-participant-form')

    context = {
        'part': part,
        'state_user': state_user,
        'form': form
    }
    return render(request, 'musabaqah/state-part.html', context)

def state_password(request):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')  # StateUser not logged in

    state_user = StateUser.objects.get(id=user_id)
    form = ChangePasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            if check_password(old_password, state_user.password):
                state_user.password = make_password(new_password)
                state_user.save()
                return redirect('state-board')
            else:
                form.add_error('old_password', 'Old password is incorrect.')

    return render(request, 'musabaqah/state-pass-change.html', {'form': form, 'state_user': state_user})

def state_forgot_password(request):
    form = StateUserForgotForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                state_user = StateUser.objects.get(email=email)
                
                # Generate a simple temporary password or token
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                # Update password (hashed)
                state_user.password = make_password(temp_password)
                state_user.save()

                # Send email
                send_mail(
                    subject="Musabaqah Password Reset",
                    message=f"Your new temporary password is: {temp_password}\nPlease log in and change it immediately.",
                    from_email="noreply@musabaqah.com",
                    recipient_list=[email],
                    fail_silently=False
                )

                messages.success(request, "A temporary password has been sent to your email.")
                return redirect('my-login')
            except StateUser.DoesNotExist:
                form.add_error('email', "No account found with that email.")

    return render(request, "musabaqah/state-forgot-password.html", {"form": form})

def state_part_view(request, pk ):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')
    state_user = StateUser.objects.get(id=user_id)
    part_v = Participant.objects.get(id=pk)
    part = Participant.objects.all()
    

    context ={'part_v':part_v,
              'part':part,
              'state_user':state_user
              }
    return render(request, 'musabaqah/state-part-view.html',context)


def update_part(request, pk):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')
    state_user = StateUser.objects.get(id=user_id)
    part_v = Participant.objects.get(id=pk)
    form = UpdateParticipantForm(instance=part_v)

    if request.method=="POST":
        
        form = UpdateParticipantForm(request.POST, request.FILES, instance=part_v)

        if form.is_valid():
            form.save()
            return redirect('state-part-view',  pk=part_v.pk)

    context ={"state_user":state_user,
              'form':form,
              'part_v':part_v        
              }
    return render(request, 'musabaqah/state-update-part.html', context)


def delete_part(request, pk):
    user_id = request.session.get('state_user_id')
    if not user_id:
        return redirect('my-login')
    state_user = StateUser.objects.get(id=user_id)
    part_v = Participant.objects.get(id=pk)

    if request.method =='POST':
        part_v.delete()
        return redirect('state-part') 

    context = {'state_user':state_user,
               'part_v':part_v
               }
    return render('musabaqah/state-part-view.html', context)


def logout_user(request):
    auth.logout(request)
    messages.success(request, 'Logout Sucessfully')
    return redirect('my-login')
