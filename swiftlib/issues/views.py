from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'issues/issues.html')

def issuebook(request):
    return render(request, 'issues/issues-add-form.html')

def returnbook(request):
    return render(request, 'issues/issues-return-form.html')

def bookinfo(request):
    return render(request, 'issues/issues-info-form.html')