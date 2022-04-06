from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from .tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# Create your views here.





#----------- FOR ADMIN REGISTRATION ---------------
def admin_account_register(request):

    if request.user.is_authenticated:
        return redirect("accounts:admin_dashboard")

    if request.method == "POST":
        registerForm = AdminRegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.is_admin = False
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMINS')
            my_admin_group[0].user_set.add(user)
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "admin/email_templates/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            messages.success(request, "Activation Link Sent on Registered Email ID.")
            return render(request, "admin/register_email_confirm.html", {"form": registerForm})
            return redirect('accounts:admin_dashboard')
    else:
        registerForm = AdminRegistrationForm()
    return render(request, "admin/admin_reg.html", {"form": registerForm})



#----------- EMAIL ACTIVATION FOR ADMIN REGISTRATION ---------------
def admin_account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_admin = True
        user.save()
        login(request, user)
        return redirect("accounts:admin_dashboard")
    else:
        return render(request, "admin/activation_invalid.html")



#----------- FOR STUDENT REGISTRATION ---------------
def student_account_register(request):
    
    if request.user.is_authenticated:
        return redirect("accounts:student_dashboard")

    if request.method == "POST":
        registerForm = StudentRegistrationForm(request.POST)
        stdExtra=StudentExtraForm(request.POST)
        if registerForm.is_valid() and stdExtra.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.is_student = False
            user.save()
            user2 = stdExtra.save(commit=False)
            user2.enrollment_no = stdExtra.cleaned_data["enrollment_no"]
            user2.user=user
            user2.save()
            my_admin_group = Group.objects.get_or_create(name='STUDENTS')
            my_admin_group[0].user_set.add(user)
            # StudentExtra.objects.create(user=user, status=False)
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "student/email_templates/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            messages.success(request, "Activation Link Sent on Registered Email ID.")
            return render(request, "student/register_email_confirm.html", {"form": registerForm, 'stdExtra':stdExtra})
    else:
        registerForm = StudentRegistrationForm()
        stdExtra=StudentExtraForm()
    return render(request, "student/stud_reg.html", {"form": registerForm, 'stdExtra':stdExtra})


#----------- EMAIL ACTIVATION FOR STUDENT REGISTRATION ---------------
def student_account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_student = True
        user.is_admin = False
        user.save()
        extra = StudentExtra.objects.get(user=user)
        extra.status = True
        extra.save()
        login(request, user)
        return redirect("accounts:student_dashboard")
    else:
        return render(request, "student/activation_invalid.html")
    
    


#-----------FOR CHECKING AN USER IS ADMIN OR STUDENT ---------------
def is_admin(user):
    return user.groups.filter(name='ADMINS').exists()
def is_student(user):
    return user.groups.filter(name='STUDENTS').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USER IS AN ADMIN OR STUDENTS
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('accounts:admin_dashboard')
    elif is_student(request.user):
        accountstatus=StudentExtra.objects.get(user_id=request.user.id)
        if accountstatus.status==True:
            return redirect('accounts:student_dashboard')
        else:
            return redirect('accounts:studentactivate')




#--------------- ADMIN DASHBOARDS & CRUD AREA ------------------
@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = Customuser.objects.all().order_by('-id')
    students = StudentExtra.objects.all().filter(status=True)
    books = Book.objects.all().filter(status=True).order_by('-id')
    context = {
        "students":students, 
        "users":users, 
        "books":books
    }
    messages.success(request, "Logged in Successfully")
    return render(request, 'admin/admin_dash.html', context)


@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def admin_edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "admin/edit_details.html", {"user_form": user_form})



@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def all_books(request):
    books = Book.objects.all().filter(status=True)
    context = {'books':books}
    return render(request, 'admin/books/all_books.html', context)



@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def add_book(request):
    bkForm = BooksForm()
    if request.method=='POST':
        bkForm =BooksForm(request.POST)
        if bkForm.is_valid():
            bkForm.save()
            return redirect('accounts:all_books')
    else:
        context = {'bkForm':bkForm}
    return render(request, 'admin/books/addbooks.html', context)



@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def update_book_details(request, pk):
    book = Book.objects.get(id=pk)
    update_book = BooksForm(request.POST or None, instance=book)
    context = {'book':book, 'update_book':update_book}
    if request.method == "POST":
        if update_book.is_valid():
            update_book.save()
            return redirect('accounts:all_books')
    
    return render(request, 'admin/books/update_book_details.html', context)



@login_required(login_url='accounts:Admin-Login')
@user_passes_test(is_admin)
def delete_book(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect('accounts:all_books')






#--------------- STUDENTS DASHBOARDS & CRUD AREA ------------------
@login_required(login_url='accounts:Student-Login')
@user_passes_test(is_student)
def student_dashboard(request):
    books = Book.objects.all().filter(status=True).order_by('-id')
    context = {'books':books}
    messages.success(request, "Logged in Successfully")
    return render(request, 'student/stud_dash.html', context)

