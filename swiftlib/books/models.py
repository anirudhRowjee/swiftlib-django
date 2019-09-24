from django.db import models

# Create your models here

class Book(models.Model):
    # defining book model

    name = models.CharField(max_length=252)
    author = models.CharField(max_length=252,null=True)
    isbn13 = models.CharField(max_length=13, blank=True)

    # book pretty name
    def pretty(self):
        authors = self.authors
        namestring = ''
        for author in authors:
            namestring += author.name + ' , '
        return self.name +' by ' + namestring






