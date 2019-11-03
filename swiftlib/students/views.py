from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student


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


# one-time function to setup default admin user
def initial_setup():
    try:
        admin_user = User.objects.get(username='admin', email='admin@swiftlib.com')
    except ObjectDoesNotExist:
        admin_user = User.objects.create_superuser(username='admin', email='admin@swiftlib.com', password='password')
        admin_user.save()

@login_required
def home(request):
    if request.method == 'POST':
        pass
    else:
        students = Student.objects.all()
        context = {
            'students': students,
        }
        return render(request, 'students/students.html', context)


@login_required
def addstudent(request):
    if request.method == 'POST':

        data = request.POST

        name = str(data.get('student-name'))
        pid = str(data.get('student-pid'))

        pid = pid.replace('/', '-')

        new_student = Student(
            name  = name,
            pid = pid
        )

        try:
            new_student.save()

        except IntegrityError:
            message = 'This student already exists!'
            return send_failure(request, message)

        message = "Student " + new_student.name + " with ID " + str(new_student.pid) + " successfully created!"
        return send_success(request, message)

    else:
        return render(request, 'students/student-add-form.html')


@login_required
def studentinfo(request, pid):
    if request.method == 'POST':
        data = request.POST
        pid = data['deletion_id']

        try:
            student_to_be_deleted = Student.objects.get(pid=pid)

        except IntegrityError:
            context = {
                'failure_message': "There is already a student with that ID!"
            }
            return render(request, 'status.html', context)

        except ObjectDoesNotExist:
            context = {
                'failure_message': "The Student you are attempting to Delete does not Exist!"
            }
            return render(request, 'status.html', context)

        student_to_be_deleted.delete()

        context = {
            'success_message': "Student " + str(pid) + " has been successfully deleted! "
        }

        return render(request, 'status.html', context)

    else:

        try:
            student = Student.objects.get(pid=pid)
            context = {
                'student': student,
            }
            return render(request,'students/student-info-form.html', context)

        except ObjectDoesNotExist:
            context = {
                'failure_message': 'Student does not exist!'
            }
            return render(request, 'status.html', context)
