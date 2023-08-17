from django.urls import path
from .views import *
urlpatterns = [
    path('', Landing_page,name='landing_page'),
    path('books/store/', product_filter_page,name='filter_books_page'),
    path('Cart/store/', cart_page,name='cart'),
    path('filters/store/', Bookfilters,name='filters'),
    path('book/detail/<str:id>/',book_details,name='book_details'),
    path('search/results/',search_result,name='search'),
    path('user_reviews/', user_reviews, name =  "user_reviews")






    ]