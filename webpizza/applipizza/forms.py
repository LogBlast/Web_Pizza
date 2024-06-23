from django import forms
from django.forms import ModelForm

from applipizza.models import Composition, Ingredient
from applipizza.models import Pizza

class IngredientForm(ModelForm):

    class Meta:
        model = Ingredient
        fields = ['nomIngredient']

class PizzaForm(ModelForm):

    class Meta:
        model = Pizza
        fields = ['nomPizza','prix']



# class IngredientForm(forms.Form) :
#     nomIngredient = forms.CharField(
#         label='nom de cet ingrédient',
#         max_length=50,
#     )

class CompositionForm(ModelForm):
    class Meta:

        model = Composition
        fields = ['ingredient','quantite']