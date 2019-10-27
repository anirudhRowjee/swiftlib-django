from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='books-home'),
    path('addbooks/', views.addbook, name='addbook'),
    path('isvalidISBN/', views.isValidISBN, name='validate_isbn'),
    path('bookinfo/<int:isbn13>', views.getbookinfo, name='bookinfo'),
]


