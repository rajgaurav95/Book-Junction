from django.urls import path
from .views import *
urlpatterns = [
    path('checkout/', checkout,name='checkout'),
    path('payment/Verify/', payment_verify, name = 'payment_verify')

]