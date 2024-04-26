from django.shortcuts import render
from django.views.generic import ListView, DetailView  #to display lists
from .models import Recipe
from .forms import RecipesSearchForm
import pandas as pd
from .utils import get_recipename_from_id, get_chart


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/main.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
# views 


def home(request):
     
     form = RecipesSearchForm(request.POST or None)
     recipes_df=None #initialize dataframe to None
     chart = None

     if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        chart_type = request.POST.get('chart_type')
        print(recipe_name, chart_type)
    

        qs =Recipe.objects.filter(name=recipe_name)
        if qs: #if data found
            #convert queryset to pandas dataframe
            recipes_df=pd.DataFrame(qs.values())
            recipes_df['id']=recipes_df['id'].apply(get_recipename_from_id)
            chart=get_chart(chart_type, recipes_df, labels=recipes_df['id'].values)
            recipes_df=recipes_df.to_html()

       
     context={
          'form': form,
         
          
     }
     return render(request, 'recipes/home.html', context)










