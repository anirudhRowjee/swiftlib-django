from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='students_home'),
    path('addstudent/', views.addstudent, name='students_add'),
    path('info/<str:pid>', views.studentinfo, name='students_info'),

]


