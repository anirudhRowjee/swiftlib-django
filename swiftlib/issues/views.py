from django.shortcuts import render
from django.db import IntegrityError
from . import models as issues
from books import models as books
from students import models as students
from datetime import datetime

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

def home(request):

    if request.method == 'POST':
        data = request.POST
        search_query = data['search_query']
        search_criteria = data['search_criteria']

        # search by book name, date or user
        if search_criteria == 'date_issued':

            search_query = search_query.replace('/', '-')
            issues_search = issues.Issue.objects.filter(date_issued=search_query)
            context = {
                'results' : issues_search,
            }
            return render(request, 'issues/issues.html', context)

        elif search_criteria == 'book_issued':
            # match the book parameters
            pass
        elif search_criteria == 'student_issued':
            # match student issued to
            pass



    else:
        return render(request, 'issues/issues.html')

def issuebook(request):
        if request.method == 'POST':
    
            data = request.POST

            student_pid = str(data['student-pid'])
            book_isbn = str(data['book-isbn'])
            
            student_issue = students.Student.objects.get(pid=student_pid)
            book_issue = books.Book.objects.get(isbn13=book_isbn)

            new_book = issues.Issue(
                user_issued = student_issue,
                book_issued = book_issue,
            )
            
            try:
                new_book.save()

            except IntegrityError:
                message = 'Book has already been issued'
                return send_failure(request, message)
        
            message = "Book "+ str(new_book.book_issued) + " has been successfully Issued! "
            
            return send_success(request, message)

        else:
            return render(request, 'issues/issues-add-form.html')

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

def issueinfo(request):
    pass
