from django.db import models

# Create your models here

class Book(models.Model):
    # defining book model

    name = models.CharField(max_length=252)
    author = models.CharField(max_length=252,null=True)
    isbn13 = models.CharField(max_length=13, blank=True, unique=True)

    # book pretty name
    def __str__(self):
        return self.name +' by ' + self.author






