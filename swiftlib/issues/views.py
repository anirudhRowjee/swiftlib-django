from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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

def get_filtered(qset, criteria):
    if criteria == 'issued_only':
        return qset.filter(status = 'issued')
    elif criteria == 'returned_only':
        return qset.filter(status = 'returned')
    else:
        return qset

@login_required
def home(request):

    if request.method == 'POST':

        data = request.POST
        search_query = data['search_query']
        search_criteria = data['search_criteria']
        filter_criteria = data['filter_criteria']

        if search_criteria == 'book_isbn':
            # search for similar ISBN of book issued
            isbn = int(search_query)
            results = issues.Issue.objects.filter(book_issued__isbn13=isbn)
            results = get_filtered(results, filter_criteria)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)

        if search_criteria == 'book_name':
            # search for similar name of book issued
            name = str(search_query)
            results = issues.Issue.objects.filter(book_issued__name__icontains=name)
            results = get_filtered(results, filter_criteria)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)

        if search_criteria == 'student_name':
            # search for similar name of student to whom book is issued
            name = str(search_query)
            results = issues.Issue.objects.filter(user_issued__name__icontains=name)
            results = get_filtered(results, filter_criteria)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)

        if search_criteria == 'student_id':
            pid = str(search_query)
            results = issues.Issue.objects.filter(user_issued__pid__icontains=pid)
            results = get_filtered(results, filter_criteria)
            context = {
                'results': results,
                'has_results': True,
            }
            return render(request, 'issues/issues.html', context)
    else:

        # default - show latest 5 issued books
        default = issues.Issue.objects.order_by('-date_issued')[:20]
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

        # check if the book has been issued toa student already
        try:
            check = students.Student.objects.get(book_issued = book_to_issue)
            if check is not None:
                return send_failure(request, "book has already been issued")
        except ObjectDoesNotExist:
            pass

        new_issue = issues.Issue(
            user_issued = student_to_issue_to,
            book_issued = book_to_issue,
            status = 'issued'
        )

        try:
            new_issue.save()
            student_to_issue_to.book_issued = book_to_issue
            student_to_issue_to.save()

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

        try:
            check = students.Student.objects.get(book_issued = book_issue)
        except ObjectDoesNotExist:
            return send_failure(request, "Book has not been issued to anyone")

        return_book = issues.Issue.objects.get(
            user_issued = student_issue,
            book_issued = book_issue,
            status = 'issued'
            )

        try:
            return_book.date_returned = now
            return_book.status = 'returned'
            return_book.save()
            student_issue.book_issued = None
            student_issue.save()

        except:
            message = 'Book could not be returned'
            return send_failure(request,message)
        message = "Book "+ str(return_book.book_issued) + " has been successfully Returned! "
        return send_success(request, message)
    else:
        return render(request, 'issues/issues-return-form.html')

def issueinfo(request, issue_id):
    #TODO - Add this method and set up modals for search results
    try:
        issue = issues.Issue.objects.get(id=issue_id)
        context = {'issue': issue}
        return render(request, 'issues/issues-info-form.html', context)

    except ObjectDoesNotExist:
        return send_failure(request, "The Issue you are looking for does not exist")
