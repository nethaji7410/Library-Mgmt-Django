from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
import re, random
from django.shortcuts import render, redirect
from .models import reader





def validate_password(pwd):
    if len(pwd) < 6:
        return "Password must be at least 6 characters."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        return "Password must contain at least one special character."
    return None


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')

        # Validate password
        error = validate_password(pwd)
        if error:
            return render(request, 'signup.html', {'error': error})

        if User.objects.filter(username=fnm).exists():
            return render(request, 'signup.html', {'error': "Username already taken."})

        otp = str(random.randint(100000, 999999))

        request.session['signup_data'] = {
            'username': fnm,
            'email': emailid,
            'password': pwd,
            'otp': otp,
        }

        send_mail(
            subject='Your OTP for Signup - Library',
            message=f'Hello {fnm}, your OTP is {otp}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[emailid],
            fail_silently=False,
        )

        return redirect('/verify_otp')

    return render(request, 'signup.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data')

        if signup_data and entered_otp == signup_data['otp']:
            new_user = User.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password'],
            )
            new_user.save()
            del request.session['signup_data']
            return redirect('/login')
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')


def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            auth_login(request, user)
            return redirect('/index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required(login_url='/login')
def signout(request):
    logout(request)
    return redirect('/login')


def home(request):
    return render(request,"home.html",context={"current_tab":"home"})

def readers(request):
    return render(request,"readers.html",context={"current_tab":"readers"})


def save_student(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        if student_name:
            return render(request, "welcome.html", context={'student_name': student_name})
    return redirect('/')

def readers_tab(request):
    readers = reader.object.all()
    return render(request,"readers.html",
                  context={"current_tab":"readers",
                           "readers":readers})
