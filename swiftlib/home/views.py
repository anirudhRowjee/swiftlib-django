from django.shortcuts import render

# Create your views here.

def home(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'home/home.html')






def login(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'home/login.html')

def create_new_user(request):
    pass

""" changelog -
1. remove quick action buttons
2. add login and logout facilities (user model)
3. finish search feature
"""

