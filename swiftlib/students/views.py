from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'students/students.html')

def addstudent(request):
    return render(request, 'students/student-add-form.html')
