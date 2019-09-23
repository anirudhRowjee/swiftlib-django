from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='books-home'),
    path('addbooks/', views.addbook, name='addbook'),
    path('bookinfo/<int:isbn>', views.getbookinfo, name='bookinfo'),
]


