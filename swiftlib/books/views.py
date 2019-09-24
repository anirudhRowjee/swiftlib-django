from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.shortcuts import render

from .models import Book

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

# Create your views here.

def home(request):
    if request.method == "POST" :
        pass
    else:
        books= Book.objects.all()
        context={
            'books' : books,
        }
    return render(request, 'books/books.html',context)

def addbook(request):
    if request.method == 'POST':

        # get all POST data from page - data submitted in form
        data = request.POST

        # reference relevant parameters
        name = str(data.get('name'))
        isbn13 = str(data.get('isbn13'))
        author=str(data.get('author'))

        # package a new Student object
        new_book = Book(
            name  = name,
            isbn13=isbn13,
            author=author
        )
        
        # save the new object
        try:
            new_book.save()

        # check if the student already exists
        except IntegrityError:
            message = 'Book already exists'
            return send_failure(request, message)

        # package success data
    
        message="Book "+ new_book.name + " added! "
        
        return send_success(request, message)

    else:
        # user wants to add data / is not reaching before any operation
        return render(request, 'books/add-book-form.html')

def getbookinfo(request, isbn13):
    if request.method == 'POST':

        data = request.POST
        isbn13 = data['delete-isbn']

        try:
            book_to_be_deleted = Book.objects.get(isbn13=isbn13)

        except ObjectDoesNotExist:
            context = {
                'failure_message': "The Book you are attempting to Delete does not Exist!"
            }
            return render(request, 'status.html', context)

        book_to_be_deleted.delete()

        context = {
            'success_message': "Book " + str(isbn13) + " has been successfully deleted! "
        }

        return render(request, 'status.html', context)

    else:

        try:
            books = Book.objects.get(isbn13=isbn13)
            context = {
                'book': books,
            }
            return render(request,'books/book-info-form.html', context)

        except ObjectDoesNotExist:
            message = 'Book does not exist'
            return send_failure(request, message)
            
    context = {
                'failure_message': 'Book does not exist!'
            }
    return render(request, 'status.html', context)
