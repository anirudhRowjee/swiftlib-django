from django.db import models
from ../books/models.py import * as book_models
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    book_issued = models.ForeignKey(book_models.Book, blank=True)


