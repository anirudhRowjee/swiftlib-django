from django.shortcuts import render
from . import models as issues
from books import models as books
from students import models as students


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
    return render(request, 'issues/issues-add-form.html')

def returnbook(request):
    return render(request, 'issues/issues-return-form.html')

def bookinfo(request):
    return render(request, 'issues/issues-info-form.html')



