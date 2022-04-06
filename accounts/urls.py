from pyexpat.errors import messages
from urllib import request
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .views import *
from .forms import *

app_name = "accounts"



urlpatterns = [
    path('adminsignup/', admin_account_register, name="admin_signup"),
    path('studentsignup/', student_account_register, name="student_signup"),
    
    #----------------------ACCOUNTS ACTIVATION URLS------------------------------------
    path("admin_activation/<slug:uidb64>/<slug:token>)/", admin_account_activate, name="adminactivate"),
    path("student_activation/<slug:uidb64>/<slug:token>)/", student_account_activate, name="studentactivate"),
    
    #---------------------- RESET PASSWOR URLS------------------------------------
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url="password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="reset_status.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/Mg/password_reset_complete/",
        TemplateView.as_view(template_name="reset_status.html"),
        name="password_reset_complete",
    ),
    
    #----------------------LOGIN URLS------------------------------------
    path('afterlogin/', afterlogin_view, name='afterlogin'),
    path('adminlogin/', auth_views.LoginView.as_view(template_name='admin/admin_login.html'), name="Admin-Login"),
    path('studentlogin/', auth_views.LoginView.as_view(template_name='student/stud_login.html'), name="Student-Login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    
    
    path('admindash/', admin_dashboard, name="admin_dashboard"),
    path("profile/edit/", admin_edit_details, name="admin_edit_details"),
    path("all_books/", all_books, name="all_books"),
    path("add_book/", add_book, name="add_book"),
    path("update_book/<int:pk>/", update_book_details, name="update_book_details"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
    
    
    path('studentdash/', student_dashboard, name="student_dashboard"),
]