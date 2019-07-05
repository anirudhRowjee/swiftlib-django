from django.db import models
from datetime import date

class Issue(models.Model):
    user_issued = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    book_issued = models.ForeignKey('issues.Issue', on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    date_returned = models.DateField()
    days = (date(date_returned)-date(date_issued)).days
    amount_collectable = '₹'+str(days*2)

    def __str__(self):
        return self.user_issued
