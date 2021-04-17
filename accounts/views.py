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
    return render(request, 'accounts/login.html')

def logout(request):
    # TODO need to route to home page and to logout
    return render(request, 'accounts/signup.html')