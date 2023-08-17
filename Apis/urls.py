from django.urls import path
from .views import *
urlpatterns = [
    path('book/cart/',CartView.as_view() ,name='book_cart'),
   

    ]