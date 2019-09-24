from django.shortcuts import render
from . import models as issues
from books import models as books
from students import models as students

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

            user_issued = str(data.get('user_issued'))
            book_issued = str(data.get('book_issued'))

            new_book = Book(
                user_issued = user_issued,
                book_issued = book_issued,
            )
            
            try:
                new_book.save()

            except IntegrityError:
                message = 'Book has already been issued'
                return send_failure(request, message)
        
            message = "Book "+ new_book.book_issued + " has been successfully Issued! "
            
            return send_success(request, message)

        else:
            return render(request, 'issues/issues-add-form.html')

def returnbook(request):
    '''http://dev.splunk.com/view/webframework-djangobindings/SP-CAAAEM5'''
    return render(request, 'issues/issues-return-form.html')

def bookinfo(request):
    return render(request, 'issues/issues-info-form.html')



