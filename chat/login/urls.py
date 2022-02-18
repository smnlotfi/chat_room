from django.urls import path,include
from .views import main,login_function



urlpatterns = [
    path('',main,name='main'),
    path('login',login_function,name='login'),
]