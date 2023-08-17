from rest_framework import serializers
from .models import *
from store.models import Book,Publisher


class PublisherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Publisher
        fields = '__all__'
class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    class Meta:
        model = Book
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemsSerializer(serializers.ModelSerializer):
    cart =CartSerializer()
    book = BookSerializer()
    class Meta:
        model = CartItems
        fields = '__all__'
