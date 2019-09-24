from django.shortcuts import render
from . import models as issues

def home(request):

    if request.method == 'POST':

        data = request.POST
        search_query = data['search_query']
        search_criteria = data['search_criteria']

        if search_criteria == 'book_isbn':
            # search for similar ISBN of book issued
            isbn = int(search_query)
            results = issues.Issue.objects.filter(book_issued__isbn13=isbn)
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
        default = issues.Issue.objects.order_by('-date_issued')[:5][::-1]
        context = {
            'has_results': False,
            'default': default,
        }
        return render(request, 'issues/issues.html', context)



def issuebook(request):
    return render(request, 'issues/issues-add-form.html')

def returnbook(request):
    return render(request, 'issues/issues-return-form.html')

def issueinfo(request):
    return render(request, 'issues/issues-info-form.html')
