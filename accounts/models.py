from unicodedata import category
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return 


class Customuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "LMSAdmin@webinoxmedia.com",
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name
    
    
    
GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


class StudentExtra(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)
    enrollment_no = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.user_name+"  [ "+str(self.enrollment_no)+" ]"
    
    @property
    def getuserid(self):
        return self.user.id
    
    

BOOKS_CAT = [
    ('Education', 'Education'),
    ('History', 'History'),
    ('Maths', 'Maths'),
    ('Biology', 'Biology'),
    ('Physics', 'Physics'),
    ('Novels', 'Novels'),
    ('Commics', 'Commics'),
    ('Sci-fi', 'Sci-fi'),
    ('Fashion', 'Fashion'),
    ('Entertainment', 'Entertainment'),
    ('Romantic', 'Romantic'),
    ('Fantacy', 'Fantacy'),
]

class Book(models.Model):
    book_no = models.PositiveIntegerField()
    book_name = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=BOOKS_CAT, blank=True)
    entry_date = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="last login", auto_now=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.book_name)
    


    
    