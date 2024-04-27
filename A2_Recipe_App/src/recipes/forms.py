from django import forms
from django.forms import ModelForm
from .models import Recipe


CHART__CHOICES = (
   
    ('#1','Bar chart'),
    ('#2', 'Pie chart'), 
    ('#3', 'Line cart')
    
)

class RecipesSearchForm(forms.Form):
    recipe_name= forms.CharField(max_length=120)
    ingredients= forms.CharField(max_length=250)
    chart_type= forms.ChoiceField(choices=CHART__CHOICES)
    #image field
    pic = forms.ImageField(required=False)


class CreateRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'cooking_time', 'pic' )
        labels = {
            'name': 'Enter the recipe name',
            'ingredients': 'List ingredients separated by a comma',
            'cooking_time': 'How many minutes does it take to cook?',
            'pic': 'Upload an image of your recipe', 

        }
        widgets = { 
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'ingredients': forms.TextInput(attrs={'class':'form-control'}),
            'cooking_time': forms.TextInput(attrs={'class':'form-control'}),
            'pic': forms.FileInput(attrs={'class':'form-control'}),
        }
        