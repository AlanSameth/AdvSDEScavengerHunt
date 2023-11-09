from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from user.forms import LocationFormSet
from user.models import User, location, Game
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
import googlemaps
from django.forms import formset_factory


# Create your views here.


class location_form(forms.Form):
    address = forms.CharField(max_length=400, label="Address", required=True)
    city = forms.CharField(max_length=400, label="City", required=True)
    country = forms.CharField(max_length=400, label="Country", required=True)
    zipcode = forms.CharField(max_length=400, label="Zipcode", required=True)
    hint = forms.CharField(max_length=400, label="Hint", required=True)
    clue = forms.CharField(max_length=400, label="Clue", required=True)

class game_form(forms.Form):
    game_name = forms.CharField(max_length=400, label="game_name", required=True)
    game_description = forms.CharField(max_length=400, label="game_description", required=True)

class approvalForm(forms.ModelForm):
    is_approved=forms.BooleanField()
    class Meta:
        model = location
        fields = ['is_approved']



def input_location(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Home"))
    if request.method == "POST":
        data = location.objects.all()
        context = {"locations": data}
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
            user_temp = User.objects.filter(user_email=request.user.email).first()
            loca.user_id=user_temp
            loca.save()

            return HttpResponseRedirect(reverse("Map"))

    else:
        form = location_form()
    return render(request, "user/new_location.html", {"form": form})


def first_page_game(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Home"))

    if request.method == "POST":
        form = game_form(request.POST)

        # print formset data if it is valid
        ga = Game()
        if form.is_valid():
            ga.game_name = form.cleaned_data["game_name"]
            ga.game_description = form.cleaned_data["game_description"]
            user_temp = User.objects.filter(user_email=request.user.email).first()
            ga.user_id = user_temp
            ga.save()

        return HttpResponseRedirect(reverse("input_game",args=(ga.id,)))
    else:
        form = game_form()
    return render(request, "user/create_game_page1.html", {"form": form})


def input_game(request,game_id):
    game_ob = get_object_or_404(Game, pk=game_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Home"))
    if request.method == "POST":
        GameFormSet = formset_factory(location_form, extra=3)
        formset = GameFormSet(request.POST)

        if formset.is_valid():
            # ga = Game()
            # ga.game_name = form.cleaned_data["game_description"]
            # ga.game_description = form.cleaned_data["game_description"]
            # user_temp = User.objects.filter(user_email=request.user.email).first()
            # ga.user_id = user_temp
            for form in formset:
                loca = location()
                loca.zipcode = form.cleaned_data["zipcode"]
                loca.city = form.cleaned_data["city"]
                loca.country = form.cleaned_data["country"]
                loca.address = form.cleaned_data["address"]
                loca.hint = form.cleaned_data["hint"]
                loca.clue = form.cleaned_data["clue"]

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
                loca.game_id=game_ob

                loca.save()

            return HttpResponseRedirect(reverse("Home"))

    else:
        GameFormSet = formset_factory(location_form, extra=3)
    return render(request, "user/create_game_page2.html", {"GameFormSet": GameFormSet})





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




def logout_user(request,game_id=None):
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


def Map(request,game_id):
    if request.user.is_authenticated:
        user_new = User.objects.filter(user_email=request.user.email).first()
        if user_new.is_admin:
            game_ob = get_object_or_404(Game, pk=game_id)
            hidden_location_list = location.objects.filter(place_id__isnull=False,game_id=game_ob)
            locations = []

            for a in hidden_location_list:
                data = {
                    'lat': float(a.latitude),
                    'lng': float(a.longitude),
                    'name': a.address
                }
                locations.append(data)
            print(locations)
            return render(request, "user/map_admin.html", {"mydata": hidden_location_list, "locations": locations,"game_id":game_id})
        else:
            game_ob = get_object_or_404(Game, pk=game_id)
            hidden_location_list = location.objects.filter(place_id__isnull=False, game_id=game_ob)
            locations = []

            for a in hidden_location_list:
                data = {
                    'lat': float(a.latitude),
                    'lng': float(a.longitude),
                    'name': a.address
                }
                locations.append(data)
            print(locations)
            return render(request, "user/map.html",{"mydata": hidden_location_list,"locations":locations})
    else:
        return HttpResponseRedirect(reverse("Home"))



def approval(request):
    if request.user.is_authenticated:
        user_new = User.objects.filter(user_email=request.user.email).first()
        if user_new.is_admin:
            if request.method == "POST":
                game_list_approved=request.POST.getlist('box')
                game_list_disapproved=request.POST.getlist('box_not')
                for i in game_list_approved:
                    Game.objects.filter(id=int(i)).update(is_approved=True,looked_by_admin=True)
                for j in game_list_disapproved:
                    Game.objects.filter(id=int(j)).update(is_approved=False,looked_by_admin=True)
                return HttpResponseRedirect(reverse("Home"))
            else:
                game_need_approval = Game.objects.filter(is_approved=False,looked_by_admin=False)
                games = []
                for a in game_need_approval:
                    data = {
                        'name': a.game_name,
                        'id': a.id,
                        'dis': a.game_description
                    }
                    games.append(data)
                return render(request, "user/approve.html", { "games": games})
        else:
            return HttpResponseRedirect(reverse("Home"))
    else:
        return HttpResponseRedirect(reverse("Home"))

def your_game(request):
    if request.user.is_authenticated:
        user_new = User.objects.filter(user_email=request.user.email).first()
        Games = Game.objects.filter( user_id=user_new)
        games = []
        for a in Games:
            data = {
                'name': a.game_name,
                'dis': a.game_description,
                'id': a.id,
                'approved': a.is_approved,
                'status': a.looked_by_admin
            }
            games.append(data)
        return render(request, "user/your_game.html", {"games": games})

    else:
        return HttpResponseRedirect(reverse("Home"))

def display_game_detail(request,game_id):
    if request.user.is_authenticated:
        game_ob = get_object_or_404(Game, pk=game_id)
        locations=location.objects.filter(game_id=game_ob)
        return render(request,"user/game_detail.html",{"locations":locations,'description': game_ob.game_description})
    else:
        return HttpResponseRedirect(reverse("Home"))


def choose_game(request):
    if request.user.is_authenticated:
        Games = Game.objects.filter(is_approved=True, looked_by_admin=True)
        return render(request, "user/choose_game.html", {"games": Games})
    else:
        return HttpResponseRedirect(reverse("Home"))

#learned how to use logout from this URL: https://www.youtube.com/watch?v=yO6PP0vEOMc
# learned more about forms from this URL: https://docs.djangoproject.com/en/4.2/topics/forms/
# learned how to use formset from this URL: https://www.geeksforgeeks.org/django-formsets/
