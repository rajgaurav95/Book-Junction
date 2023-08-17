from django.shortcuts import render
import razorpay
import json
from django.http import JsonResponse,HttpResponse
from .models import * 
from Apis.models import *
# Create your views here.
client = razorpay.Client(auth=("rzp_test_CIYSLCOiFiupZ8", "LCGiPNrCEw13ibJ9XFlwy8SA"))

def checkout(request):
    data ={}
    context = {}
    user = request.user
    cart = Cart.objects.filter(user=user,ordered=False).first()
    queryset = CartItems.objects.filter(cart=cart)
    total = queryset[0].get_total_qty(queryset)
    books = queryset[0].get_books(queryset)
    print(total)
    order_amount = total *100
    name = user.get_full_name()
    email= user.email
        
                    
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    data['order_curruncy']=order_currency
    notes = {
            'Shipping address': 'Bommanahalli, Bangalore'
            }
        
    response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        
    order_id = response['id']
    order_status = response['status']
    data['order_id']=order_id
    data['order_status']=order_status
       
    if order_status=='created':
    
        context['total'] = total
        context['name'] = name
        context['phone'] = ''
        context['email'] = email
        context['books'] = books

        
        # data that'll be send to the razorpay for
        context['order_id'] = order_id
        # context['my_order_id']=my_order.id
        return render(request, 'payment_gateway/confirm_order.html',context)
    return HttpResponse('<h1>Error in  create order function</h1>')
   

#Razor pay payment status after successfull payment
def payment_verify(request):
    if request.method =='POST':
        response = request.POST
        params_dict = {
            'razorpay_payment_id' : response['payment_id'],
            'razorpay_order_id' : response['order_id'],
            'razorpay_signature' : response['signature']
        }
        
        # VERIFYING SIGNATURE
        status = client.utility.verify_payment_signature(params_dict)
        if status:
            return JsonResponse({'success':False})
        else:
            razor_obj=RazorPayDetails.objects.create(razorpay_payment_id=params_dict['razorpay_payment_id'],razorpay_order_id=params_dict['razorpay_order_id'],razorpay_signature=params_dict['razorpay_signature'])
            return JsonResponse({'success':True})
