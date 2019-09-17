from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.app_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
