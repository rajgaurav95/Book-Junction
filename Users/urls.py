from django.urls import path
from .views import *
urlpatterns = [
    path('register/',AuthRegisterView.as_view() ,name='register'),
    path('Login/',AuthLoginView.as_view() ,name='login'),
    path('Logout/',Logout ,name='logout'),


   

    ]