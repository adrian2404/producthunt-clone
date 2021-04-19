from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def signup(request):
    if request.method == 'POST':
        # user has entered the info and wants to sign up
        username, password, confirmed_password = request.POST['username'], request.POST['password'], \
                                                 request.POST['confirmed_password']
        if password == confirmed_password:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username, password=password)
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/signup.html',
                              {'error': 'Username {} has already been taken'.format(username)})
        else:
            return render(request, 'accounts/signup.html',
                          {'error': 'Passwords must match'})
    else:
        # user wants to enter the info
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',
                          {'error': 'Username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')