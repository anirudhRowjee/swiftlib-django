from django.shortcuts import render
from .models import Issues
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


def send_success(request, message):
    context = {
        'failure_message': message
        }
    return render(request, 'status.html', context)

def send_failure(request, message):
    context = {
        'failure_message': message
        }
    return render(request, 'status.html', context)


# main function body

def home(request):
    if request.method == 'POST':
        pass
    else:
        issues = Issue.objects.all()
        context = {
            'issues': issues,
        }
        return render(request, 'issues.html', context)  



def issuebook(request):

    if request.method == 'POST':

        # get all POST data from page - data submitted in form
        data = request.POST

        # reference relevant parameters
        bookname = str(data.get('student-name'))
        pid = str(data.get('student-pid'))

        # replace '-' with '/'
        isbn=isbn.replace('/','-')
        pid = pid.replace('/', '-')

        # package a new issuebook object
        issuebook = Issue(
            bookname  = bookname,
            pid = pid,
            isbn=isbn
        )

        # save the new object
        try:
            issuebook.save()

        # check if the book has already been issued
        except IntegrityError:
            message = 'This book has already been issued!'
            return send_failure(request, message)

        # package success data
        context = {
            'success_message': "Book - " + issuebook.bookname + "has been issued succesfully" 
        }
        # render the success message page
        return render(request, 'status.html', context)

    else:
        return render(request, 'issues/issues-add-form.html')



def returnbook(request, bookname):

    if request.method == 'POST':

        data = request.POST

        student_id = data['student_id']
        ISBN = data['ISBN']

        try:
            #updating return_date field

            q="update Issue set date_returned =" + date.today() + "where book_issued =" + str(bookname) "

            Issue.objects.raw(q)

        except ObjectDoesNotExist:

            context = {
                'failure_message': "The Book you are attempting to Return has not been issued!"
            }
            return render(request, 'status.html', context)

        
        context = {
            'success_message': "Book " + bookname + " has been successfully returned! "
        }

        return render(request, 'issues/issues-return-form.html')

def bookinfo(request)

        try:
            # get issues info we need to return

            issues = Issue.objects.get(bookname=bookname)

            context = {
                'issues': issues,
            }

            return render(request,'issues/issue-info-form.html', context)

        except ObjectDoesNotExist:
            context = {
                'failure_message': 'Book does not exist!'
            }
            return render(request, 'status.html', context)
