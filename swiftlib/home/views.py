from django.shortcuts import render

# Create your views here.

def home(request):
    pass

def opstat(request):
    return render(request, 'status.html')
