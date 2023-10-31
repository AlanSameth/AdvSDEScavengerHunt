from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from user.models import User, location
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
import googlemaps

# Create your views here.


class location_form(forms.Form):
    zipcode = forms.CharField(max_length=400,label="zipcode",required=True)
    city = forms.CharField(max_length=400,label="city",required=True)
    country = forms.CharField(max_length=400,label="country",required=True)
    address = forms.CharField(max_length=400, label="address",required=True)

def input_location(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Home"))
    if request.method == "POST":
        form = location_form(request.POST)
        if form.is_valid():
            loca = location()
            loca.zipcode = form.cleaned_data["zipcode"]
            loca.city = form.cleaned_data["city"]
            loca.country = form.cleaned_data["country"]
            loca.address = form.cleaned_data["address"]

            if location.objects.filter(zipcode=loca.zipcode,city=loca.city,country=loca.country,address=loca.address).first() is not None:
                # if we can show a message here? like the location is already marked
                return HttpResponseRedirect(reverse("Map"))
            adress_string = str(loca.address) + ", " + str(loca.zipcode) + ", " + str(
                loca.city) + ", " + str(loca.country)
            gmaps = googlemaps.Client(key='AIzaSyCZuOZgsa4NguR95jd7NL1C4Ov01ozSbbc')
            result = gmaps.geocode(adress_string)[0]
            lat = result.get('geometry', {}).get('location', {}).get('lat', None)
            lng = result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id = result.get('place_id', {})

            loca.latitude = lat
            loca.longitude = lng
            loca.place_id = place_id
            loca.save()

            return HttpResponseRedirect(reverse("Map"))

    else:
        form = location_form()
    return render(request, "user/new_location.html", {"form": form})

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
    if request.user.is_authenticated:
        user_new = User.objects.filter(user_email=request.user.email).first()
        if user_new.is_admin:
            hidden_location_list = location.objects.filter(place_id__isnull=False)
            locations = []

            for a in hidden_location_list:
                data = {
                    'lat': float(a.latitude),
                    'lng': float(a.longitude),
                    'name': a.address
                }
                locations.append(data)
            print(locations)
            return render(request, "user/map_admin.html", {"mydata": hidden_location_list,"locations":locations})
        else:
            return render(request, "user/map.html")
    else:
        return HttpResponseRedirect(reverse("Home"))








#learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc
# learned more about forms from this URL: https://docs.djangoproject.com/en/4.2/topics/forms/