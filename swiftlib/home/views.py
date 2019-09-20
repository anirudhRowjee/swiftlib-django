from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

# Create your views here.

def send_success(request, message):
    context = {
        'success_message': message
        }
    return render(request, 'status.html', context)

def send_failure(request, message):
    context = {
        'failure_message': message
    }
    return render(request, 'status.html', context)


@login_required
def home(request):
    librarians = User.objects.all()
    return render(request, 'home/home.html', {'libs':librarians})

def app_login(request):
    if request.method == 'POST':
        # login 
        data = request.POST
        username = data['username']
        password = data['password']

        user1 = auth.authenticate(request, username=username, password=password)

        if user1 is not None:
            auth.login(request, user1)
            return redirect('home')

        elif user1 is None:
            context = {
                'error': "User Credentials Invalid"
                }
            return render(request, 'home/login.html', context)
    else:
        return render(request, 'home/login.html')

@login_required
def create_new_user(request):

    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        if password1 == password2:
            try:
                user = User.objects.create(username=username, password=password1)
            except IntegrityError:
                return send_failure(request, "User Already Exists!")

            message = "Librarian {username} successfully created!".format(username=user.username)
            return send_success(request, message)
        else:
            message = 'Passwords do not match!'
            return send_failure(request, message)
    else:
        return render(request, 'home/add-user.html')

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('login')

""" changelog -
1. remove quick action buttons
2. finish search feature
"""

