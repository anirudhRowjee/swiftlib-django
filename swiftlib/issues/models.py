from django.db import models

class Issue(models.Model):

    status_options = [('issued', 'ISSUED'),
                       ('returned', 'RETURNED')]

    user_issued = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    book_issued = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    date_returned = models.DateField(blank=True,null=True)
    status = models.CharField(max_length=8, choices= status_options, default='issued')

    def __str__(self):
        return str(self.user_issued)  + " borrowed " +  str(self.book_issued)
