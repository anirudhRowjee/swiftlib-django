from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Student
# Create your views here.

def home(request):
    if request.method == 'POST':
        pass
    else:
        students = Student.objects.all()
        context = {
            'students': students,
        }
        return render(request, 'students/students.html', context)

def addstudent(request):
    if request.method == 'POST':
        # create new student object
        data = request.POST
        name = str(data.get('student-name'))
        pid = str(data.get('student-pid'))
        # escape all slash characters '/' with dashes '-'
        '''
        This is because using / causes the url router to break -
        out format is 'info/<str:pid>', but if our pid is AA/BB/CC,
        then our router transfers us to 'info/AA/BB/CC', which does not exist
        as our URLs are not configured so deep
        '''
        pid = pid.replace('/', '-')
        new_student = Student(
            name  = name,
            pid = pid
        )
        new_student.save()
        context = {
            'success_message': "Student " + new_student.name + " with ID " + str(new_student.pid) + " successfully created!"
        }
        return render(request, 'status.html', context)
    else:
        return render(request, 'students/student-add-form.html')

def studentinfo(request, pid):
    try:
        student = Student.objects.get(pid=pid)
        context = {
            'student': student,
        }
    except ObjectDoesNotExist:
        context = {
            'failure_message': 'Student does not exist!'
        }
        return render(request, 'status.html', context)

    return render(request,'students/student-info-form.html', context)
