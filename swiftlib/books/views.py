from django.shortcuts import render

# Create your views here.

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
    return render(request, 'books/books.html')

def addbook(request):
    return render(request, 'books/add-book-form.html')

def getbookinfo(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'books/book-info-form.html')  



