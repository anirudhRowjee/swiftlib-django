from django.shortcuts import render
from django.db import IntegrityError
from datetime import datetime
from . import models as issues
from books import models as books
from students import models as students
from django.contrib.auth.decorators import login_required

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

@login_required
def home(request):

    if request.method == 'POST':

        data = request.POST
        search_query = data['search_query']
        search_criteria = data['search_criteria']

        if search_criteria == 'book_isbn':
            # search for similar ISBN of book issued
            isbn = int(search_query)
            results = issues.Issue.objects.filter(book_issued__isbn13=isbn).filter(date_returned=None)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)

        if search_criteria == 'book_name':
            # search for similar name of book issued
            name = str(search_query)
            results = issues.Issue.objects.filter(book_issued__name__icontains=name)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)

        if search_criteria == 'student_name':
            # search for similar name of student to whom book is issued
            name = str(search_query)
            results = issues.Issue.objects.filter(user_issued__name__icontains=name)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)
    else:

        # default - show latest 5 issued books
        default = issues.Issue.objects.order_by('-date_issued')
        context = {
            'has_results': False,
            'default': default,
        }
        return render(request, 'issues/issues.html', context)


@login_required
def issuebook(request):
    if request.method == 'POST':

        data = request.POST
        student_pid = str(data['student-pid'])
        book_isbn = str(data['book-isbn'])

        student_to_issue_to = students.Student.objects.get(pid=student_pid)
        book_to_issue = books.Book.objects.get(isbn13=book_isbn)

        new_issue = issues.Issue(
            user_issued = student_to_issue_to,
            book_issued = book_to_issue,
        )

        try:
            new_issue.save()
            student_to_issue_to.book_issued = book_to_issue

        except IntegrityError:
            message = 'Book has already been issued'
            return send_failure(request, message)

        message = "Book "+ str(new_issue.book_issued) + " has been successfully Issued! "

        return send_success(request, message)

    else:
        return render(request, 'issues/issues-add-form.html')

@login_required
def returnbook(request):
    if request.method == 'POST':

        now = datetime.today().strftime('%Y-%m-%d')

        data = request.POST

        student_pid = str(data['student-pid'])
        book_isbn = str(data['book-isbn'])

        student_issue = students.Student.objects.get(pid=student_pid)
        book_issue = books.Book.objects.get(isbn13=book_isbn)

        return_book = issues.Issue.objects.get(
            user_issued = student_issue,
            book_issued = book_issue
            )

        try:
            return_book.date_returned = now
            return_book.save()

        except:
            message = 'Book could not be returned'
            return send_failure(request,message)
        message = "Book "+ str(return_book.book_issued) + " has been successfully Returned! "
        return send_success(request, message)
    else:
        return render(request, 'issues/issues-return-form.html')



@login_required
def issueinfo(request):
    if request.method == 'GET':
        #TODO - Add this method and set up modals for search results
        pass
    else:
        pass
