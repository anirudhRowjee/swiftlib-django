from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/home.html')




def login(request):
    pass

def create_new_user(request):
    pass
