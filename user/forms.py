from django import forms
from django.forms import inlineformset_factory, ModelForm

from .models import Game, location

class GameForm(ModelForm):
    class Meta:
        model = location
        fields = ['zipcode', 'city', 'country','address','hint']

LocationFormSet = inlineformset_factory(Game, location, form = GameForm,
                                        extra=3, can_delete = False, min_num=3)

