from django.db import models

# Create your models here.


class Author(models.Model):
    # defining authors model
    name = models.CharField(max_length=252)

    # return author name for reference
    def __str__(self):
        return self.name


class Book(models.Model):
    # defining book model

    name = models.CharField(max_length=252)
    author = models.ManyToManyField(Author)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    costprice = models.DecimalField(decimal_places=2, max_digits=7)

    # book pretty name
    def pretty(self):
        authors = self.authors
        namestring = ''
        for author in authors:
            namestring += author.name + ' , '
        return self.name +' by ' + namestring






