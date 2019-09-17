from django.shortcuts import render, redirect
from django.contrib import auth

# Create your views here.

def home(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'home/home.html')

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

def create_new_user(request):
    pass

def logout_view(request):
    auth.logout(request)
    return render(request, 'home/login.html')

""" changelog -
1. remove quick action buttons
2. finish search feature
"""

