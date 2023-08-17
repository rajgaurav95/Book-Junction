from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.



class CartView(APIView):
    
    def get(self , request):
        user = request.user
        cart = Cart.objects.filter(user=user,ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self , request):
        data = request.data
        user = request.user
        cart,_=Cart.objects.get_or_create(user=user,ordered=False)
        book = Book.objects.get(id=int(data.get('product')))
        price = book.price
        quantity=data.get('quantity')
        cart_items = CartItems(cart=cart,user=user,book=book,price=price,quantity=quantity)
        cart_items.save()

        total_price = 0
        cart_items = CartItems.objects.filter(user=user,cart=cart.id)
        for item in cart_items:
            total_price +=item.price
        cart.total_price = total_price
        cart.save()
        return Response({
            'success': 'Items added to your cart'
        })


    
    def put(self , request):
        data = request.data
        print(int(data.get('id')[0]))
        cart_item = CartItems.objects.get(id=int(data.get('id')[0]))
        print(cart_item.__dict__)
        if data.get('sign') == '+':
            cart_item.quantity+=1
        if data.get('sign') == '-':
            cart_item.quantity-=1
        
        cart_item.save()
        return Response({
            'success': True
        })



    
    def delete(self , request):
        data = request.data
        user=request.user
        cart_item = CartItems.objects.get(id=int(data.get('id')))
        cart_item.delete()

        # cart=Cart.objects.filter(user=user,ordered=False).first()
        # queryset = CartItemss.objects.filter(cart=cart)
        # serializer = CartItemsSerializer(queryset,many=True)
        return Response({'success':True})