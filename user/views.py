from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

def home_page(request):

    return render(request,"home.html")

def logout_user(request):
    logout(request)
    return redirect('/')

#learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc