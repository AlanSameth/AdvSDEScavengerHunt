from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.views.generic import CreateView

from user.forms import LocationFormSet
from user.models import User, location, Game
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
import googlemaps


# Create your views here.


class location_form(forms.Form):
    address = forms.CharField(max_length=400, label="Address", required=True)
    city = forms.CharField(max_length=400, label="City", required=True)
    country = forms.CharField(max_length=400, label="Country", required=True)
    zipcode = forms.CharField(max_length=400, label="Zipcode", required=True)
    hint = forms.CharField(max_length=400, label="Hint", required=True)
    clue = forms.CharField(max_length=400, label="Clue", required=True)


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
            loca.hint = form.cleaned_data["hint"]
            loca.clue = form.cleaned_data["clue"]

            if location.objects.filter(zipcode=loca.zipcode, city=loca.city, country=loca.country,
                                       address=loca.address).first() is not None:
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
        user_new = User.objects.filter(user_email=request.user.email).first()
        if user_new is not None:
            user_new.user_name = request.user.username
            user_new.save()
            if user_new.is_admin:
                return render(request, "user/admin_home.html", {"admin": user_new})
            else:
                return render(request, "user/home.html")
        else:
            user_tosave = User(user_name=request.user.username, user_email=request.user.email)
            user_tosave.save()
    return render(request, "user/home.html")


def logout_user(request):
    logout(request)
    return redirect('/')


class SubmissionView(CreateView):
    model = Game
    fields = ['game_name']
    #figure out template
    #figure out success url
    def get_context_data(self, **kwargs):
        data = super(SubmissionView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['game'] = LocationFormSet(self.request.POST)
        else:
            data['game'] = LocationFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        game = context['game']
        with transaction.atomic():
            self.object = form.save()

            if game.is_valid():
                game.instance = self.object
                game.save()
        return super(SubmissionView, self).form_valid(form)


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
            return render(request, "user/map_admin.html", {"mydata": hidden_location_list, "locations": locations})
        else:
            return render(request, "user/map.html")
    else:
        return HttpResponseRedirect(reverse("Home"))

# learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc
# learned more about forms from this URL: https://docs.djangoproject.com/en/4.2/topics/forms/
