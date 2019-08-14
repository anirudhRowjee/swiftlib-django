from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='issues-home'),
    path('issue-book', views.issuebook, name='issuebook'),
    path('returnbooks/', views.returnbook, name='returnbook'),
    path('bookinfo/', views.bookinfo, name='bookinfo')
]
