from django.db import models

# Create your models here.
class RazorPayDetails(models.Model): 
    razorpay_payment_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=250,null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)