from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Student

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
        new_student.save()

        # package success data
        context = {
            'success_message': "Student " + new_student.name + " with ID " + str(new_student.pid) + " successfully created!"
        }
        # render the success message page
        return render(request, 'status.html', context)

    else:
        # user wants to add data / is not reaching before any operation
        return render(request, 'students/student-add-form.html')



def studentinfo(request, pid):

    if request.method == 'POST':

        # get ID of student to be deleted form POST data
        data = request.POST

        # assign that ID to locally-referenceable variable PID
        pid = data['deletion_id']

        try:
            # get relevant student object
            student_to_be_deleted = Student.objects.get(pid=pid)

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

