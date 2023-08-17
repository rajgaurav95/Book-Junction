from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from .models import CustomUser
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2",'first_name','last_name','phone')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username=self.cleaned_data["email"]
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        user.phone=self.cleaned_data["phone"]

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user
    
    def clean(self):
        form_data = self.cleaned_data
        email=form_data.get("email")
        phone=form_data.get("phone")


        try:
            user_e=CustomUser.objects.get(email=email)

        except:
            user_e=None

        try:
            user_p=CustomUser.objects.get(phone=phone)

        except:
            user_p=None
        if user_e:
            raise ValidationError("email is already exist")
        if user_p:
            raise ValidationError("Phone number is already exist")

        password1 = form_data.get("password1")
        password2 = form_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords did not match")
        return form_data