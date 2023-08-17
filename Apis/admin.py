from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','ordered','total_price')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','user','book','price','quantity')


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems,CartItemAdmin)

