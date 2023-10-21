from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from user.models import User, location
from django.urls import reverse
from django.views.generic import ListView

# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
        user_new=User.objects.filter(user_email=request.user.email).first()
        if user_new is not None:
            user_new.user_name = request.user.username
            user_new.save()
            if user_new.is_admin:
                return render(request,"user/admin_home.html",{"admin":user_new})
            else:
                return render(request, "user/home.html")
        else:
            user_tosave=User(user_name=request.user.username,user_email=request.user.email)
            user_tosave.save()
    return render(request, "user/home.html")

def logout_user(request):
    logout(request)
    return redirect('/')



def Map(request):
    return render(request, "user/map.html")

def map_admin(request):
    hidden_location_list = location.objects.all()
    return render(request,"user/map_admin.html",{"mydata":hidden_location_list})







#learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc