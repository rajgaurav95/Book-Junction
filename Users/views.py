#Standard library imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
import random
import threading
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login


#Related third party imports.
from passlib.hash import django_pbkdf2_sha256 as handler


#Local application/library specific imports.
from Users.forms import SignUpForm
# from Users.models import OTP

# Create your views here.
# User Register View
class AuthRegisterView(View):
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, f"You have successfully registerd")
            return render(request,'signin.html')

        for msg in form.error_messages:
            messages.error(request, f"{msg}: {form.error_messages[msg]}")


        return render(request, self.template_name)


class AuthLoginView(View):
    form_class = SignUpForm
    template_name = 'signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        try:
            user = authenticate(email = email, password = password)
        except:
            user = None
        if user:
            login(request, user)
            return redirect('/')
        messages.error(request,f"email or password is incorrect")
        return render(request, self.template_name)

def Logout(request):
    logout(request)
    return redirect('/')