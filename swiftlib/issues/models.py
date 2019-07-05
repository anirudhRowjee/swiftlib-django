from django.db import models

class Issue(models.Model):
    user_issued=models.ForeignKey('students.Student', on_delete=models.CASCADE)
    book_issued=models.ForeignKey('issues.Issue', on_delete=models.CASCADE)

