from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'issues/issues.html')

def issuebook(request):
    return render(request, 'issues/issues-add-form.html')
