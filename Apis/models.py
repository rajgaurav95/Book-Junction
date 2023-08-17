from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from Users.models import CustomUser
from store.models import Book
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.email) + " " + str(self.total_price)
         


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.email) + " " + str(self.book.title)
    def get_total_qty(self,qs):
        total = 0
        for obj in qs:
            total += obj.price * obj.quantity
        return total

    def get_books(self,qs):
        books = [ obj.book.title for obj in qs ]
        return books


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_book = Book.objects.get(id=cart_items.book.id)
    cart_items.price = float(cart_items.quantity) * float(price_of_book.price)
    total_cart_items = CartItems.objects.filter(user = cart_items.user )
    cart = Cart.objects.get(id = cart_items.cart.id)
    cart.total_price = cart_items.price
    cart.save()

