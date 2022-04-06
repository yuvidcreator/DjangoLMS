from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import *
from django.db import transaction
from django.contrib.auth.models import Group






class AdminRegistrationForm(forms.ModelForm):

    user_name = forms.CharField(label="Enter Username", min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        max_length=100, help_text="Required", error_messages={"required": "Sorry, you will need an email"}
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Customuser
        fields = (
            "user_name",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = Customuser.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customuser.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update({"class": "field", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "field", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "field", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat Password"})

    
    



class StudentRegistrationForm(forms.ModelForm):

    user_name = forms.CharField(label="Enter Username", min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        max_length=100, help_text="Required", error_messages={"required": "Sorry, you will need an email"}
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Customuser
        fields = (
            "user_name",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = Customuser.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customuser.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat Password"})




class StudentExtraForm(forms.ModelForm):
    enrollment_no = forms.CharField(label="Roll No", min_length=4, max_length=50)
    
    class Meta:
        model=StudentExtra
        fields = [ "enrollment_no" ]




class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "Registered Email ID", "id": "login-username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )
    
    
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "Enter Registered Email", "id": "form-email"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = Customuser.objects.filter(email=email)
        if not u:
            raise forms.ValidationError("Unfortunatley we can not find that email address")



class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "field", "placeholder": "New Password", "id": "form-newpass"}
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "field", "placeholder": "New Password", "id": "form-new-pass2"}
        ),
    )
    


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )

    user_name = forms.CharField(
        label="Account Username (can not be changed)",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "field",
                "placeholder": "Username",
                "id": "form-username",
                "readonly": "readonly",
            }
        ),
    )

    first_name = forms.CharField(
        label="Firstname",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "Firstname", "id": "form-firstname"}
        ),
    )
    
    last_name = forms.CharField(
        label="Lastname",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "Lastname", "id": "form-lastname"}
        ),
    )
    
    mobile = forms.CharField(
        label="Mobile No",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "field", "placeholder": "Mobile No", "id": "form-mobileno"}
        ),
    )

    class Meta:
        model = Customuser
        fields = (
            "email",
            "user_name",
            "first_name",
            "last_name",
            "mobile",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True





class BooksForm(forms.ModelForm):
    
    class Meta:
        model=Book
        fields=['book_no','book_name','author','category']