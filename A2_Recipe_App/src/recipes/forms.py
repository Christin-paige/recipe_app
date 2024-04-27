from django import forms

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
