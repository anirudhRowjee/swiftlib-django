from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from .models import Book
from .libs import getBookData

import json

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

def validateISBN(isbn):
    return str(''.join([x for x in isbn if x.isdigit()]))

# Create your views here.

@login_required
def home(request):
    if request.method == "POST" :
        pass
    else:
        books= Book.objects.all()
        context={
            'books' : books,
        }
    return render(request, 'books/books.html',context)

@login_required
def addbook(request):
    if request.method == 'POST':

        # get all POST data from page - data submitted in form
        data = request.POST

        # reference relevant parameters
        name = str(data.get('name'))
        isbn13 = str(data.get('isbn13'))
        author=str(data.get('author'))

        isbn13 = validateISBN(isbn13)

           # package a new Book object
        new_book = Book(
            name  = name,
            isbn13=isbn13,
            author=author
        )

        # save the new object
        try:
            new_book.save()

        # check if the book already exists
        except IntegrityError:
            message = 'Book already exists'
            return send_failure(request, message)

        # package success data

        message="Book "+ new_book.name + " added! "

        return send_success(request, message)

    else:
        # user wants to add data / is not reaching before any operation
        return render(request, 'books/add-book-form.html')

@login_required
def isValidISBN(request):
    if request.method == 'GET':
        data = request.GET
        isbn = data['isbn']
        isbn = validateISBN(isbn)

        data = getBookData(isbn)

        if data is False:
            return JsonResponse({'status':'failure'}) 
        else:
            return_data = {
                'status': 'found',
                'isbn13': data[2],
                'name': data[0],
                'author': data[1]
            }
            return JsonResponse(return_data)

@login_required
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
