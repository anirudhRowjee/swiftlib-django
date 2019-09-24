from django.db import models

class Issue(models.Model):
    user_issued = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    book_issued = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    date_returned = models.DateField(blank=True)

    def __str__(self):
        return self.user_issued  + " borrowed " +  self.book_issued
