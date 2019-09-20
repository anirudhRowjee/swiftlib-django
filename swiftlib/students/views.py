# importing error classes
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# importing login-required decorator
from django.contrib.auth.decorators import login_required

#import render to return pages
from django.shortcuts import render

# import models
from .models import Student

# success and error message classes

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


# main function body

@login_required
def home(request):
    if request.method == 'POST':
        # blank method - we are not accepting any data through POST
        pass
    else:
        students = Student.objects.all()
        context = {
            'students': students,
        }
        return render(request, 'students/students.html', context)

@login_required
def addstudent(request):
    # see if we are submitting data or querying for the page
    if request.method == 'POST':

        # get all POST data from page - data submitted in form
        data = request.POST

        # reference relevant parameters
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

        # package a new Student object
        new_student = Student(
            name  = name,
            pid = pid
        )

        # save the new object
        try:
            new_student.save()

        # check if the student already exists
        except IntegrityError:
            message = 'This student already exists!'
            return send_failure(request, message)

        # package success data
        message = "Student " + new_student.name + " with ID " + str(new_student.pid) + " successfully created!"

        send_success(request, message)

    else:
        # user wants to add data / is not reaching before any operation
        return render(request, 'students/student-add-form.html')

@login_required
def studentinfo(request, pid):
    if request.method == 'POST':
        # get ID of student to be deleted form POST data
        data = request.POST
        # assign that ID to locally-referenceable variable PID
        pid = data['deletion_id']
        try:
            # get relevant student object
            student_to_be_deleted = Student.objects.get(pid=pid)
        except IntegrityError:
            # catch duplicate IDs
            context = {
                'failure_message': "There is already a student with that ID!"
            }
            return render(request, 'status.html', context)
        except ObjectDoesNotExist:
            context = {
                'failure_message': "The Student you are attempting to Delete does not Exist!"
            }
            return render(request, 'status.html', context)
        # now that we have ensured that the student exists, we perform the deletion
        student_to_be_deleted.delete()
        context = {
            'success_message': "Student " + str(pid) + " has been successfully deleted! "
        }
        return render(request, 'status.html', context)
    else:
        try:
            # get student object whose data we need to return
            student = Student.objects.get(pid=pid)
            context = {
                'student': student,
            }
            return render(request,'students/student-info-form.html', context)
        except ObjectDoesNotExist:
            # if the student does not exist, we handle this error
            context = {
                'failure_message': 'Student does not exist!'
            }
            return render(request, 'status.html', context)
