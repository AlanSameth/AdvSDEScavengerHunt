from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from user.models import User
from django.urls import reverse

# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
        user_new=User.objects.filter(user_name=request.user.username).first()
        if user_new is not None and user_new.is_admin:
            return render(request,"user/admin_home.html",{"admin":user_new})

        user_tosave=User(user_name=request.user.username,user_email=request.user.email)
        user_tosave.save()
    return render(request, "user/home.html")

def logout_user(request):
    logout(request)
    return redirect('/')




#learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc