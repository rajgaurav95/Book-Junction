from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from Users.models import CustomUser


class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Publisher(models.Model):
    name = models.CharField(max_length = 100)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


def cover_upload_path(instance, filename):
    return '/'.join(['books', str(instance.id), filename])

class genres(models.Model):
    name=models.CharField(max_length = 200)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name
    def get_book_count(self):
        return self.books.all().count()


class Book(models.Model):
    isbn = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE)
    description = models.TextField()
    publish_date = models.DateField(default = timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=0)
    edition = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to=cover_upload_path, default='books/empty_cover.jpg')
    genre=models.ManyToManyField(genres,through='book_genres',related_name='books')
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.title
    def get_genre(self):
        all_gen=''
        q=self.genre.all()
        for i in range(len(q)):
            if i == len(q)-1:
                all_gen+=q[i].name
            else:
                all_gen+=q[i].name+" ,"
        return all_gen


class book_genres(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    genre=models.ForeignKey(genres,on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    publish_date = models.DateField(default = timezone.now)
    text = models.TextField()
    rate = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)



class Discount(models.Model):
    customer=models.ManyToManyField(CustomUser,related_name='books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate= models.IntegerField()
    name= models.CharField(max_length = 200)


class RazorPayDetails(models.Model): 
    razorpay_payment_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=250,null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    date= models.DateTimeField(auto_now=True,blank=True,null=True)
    order_curruncy=models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False)
    razorpay = models.ForeignKey(RazorPayDetails, on_delete=models.CASCADE,null=True,blank=True)
    discounts = models.ForeignKey(Discount, on_delete=models.CASCADE,null=True,blank=True)



    def add_to_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            preexistting_order = BookOrder.objects.get(book=book, cart=self)
            preexistting_order.quantity +=1
            preexistting_order.save()
        except BookOrder.DoesNotExist:
            new_order = BookOrder.objects.create(
                book = book,
                cart = self,
                quantity = 1
            )

    def remove_from_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            preexistting_order = BookOrder.objects.get(book=book, cart=self)
            if preexistting_order.quantity > 1:
                preexistting_order.quantity -=1
                preexistting_order.save()
            else:
                preexistting_order.delete()
        except BookOrder.DoesNotExist:
            pass


class BookOrder(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()



class Category(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    