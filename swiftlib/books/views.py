from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'books/books.html')

def addbook(request):
    return render(request, 'books/add-book-form.html')



