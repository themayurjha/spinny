from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from products.views import *
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import  messages


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["your_pass"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('products/')
        else:
            return render(request, 'login/index.html', {'message': "Invalid Username or Password"})
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('products/')
        else:
            try:
                msg = ''
                storage = messages.get_messages(request)
                for messg in storage:
                    msg = messg
            except Exception as e:
                pass
            return render(request, 'login/index.html', {'message': msg})



def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/products/')
        else:
            return render(request, 'login/signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        email = request.POST['email']
        repass = request.POST ['re_pass']
        account_type = request.POST['account_type']

        if password == repass:
            if account_type == 'Select Type of Account':
                return render(request, 'login/signup.html', {'message': "Please Select type of account from dropdown"})
            else:
                try:
                    try:
                        check_user = User.objects.get(username=username)
                    except Exception as e:
                        check_user = False
                    if check_user:
                        return render(request, 'login/signup.html', {'message': "Username Already Exists"})
                    else:
                        try:
                            check_email = User.objects.get(email=email)
                        except Exception as e:
                            check_email = False
                        if check_email:
                            return render(request, 'login/signup.html', {'message': "Email Already Exists"})
                        else:
                            if account_type == 'staff':
                                user = User.objects.create_user(username=username, password=password, email=email, is_staff=True)
                            else:
                                user = User.objects.create_user(username=username, password=password, email=email)
                            user.save()
                            messages.add_message(request, messages.INFO, "Registration Successfull. Please login to Continue")
                            return redirect('/')

                except Exception as e:
                    return render(request, 'login/signup.html', {'message': "Something Went Wrong. Please Try Again."})
        else:
            return render(request, 'login/signup.html', {'message': "Password Doesn't match"})

def logout(request):
    auth.logout(request)
    return redirect('/')