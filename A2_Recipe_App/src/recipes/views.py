from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from .utils import get_recipe_ingredient_usage, get_recipename_from_id
from .forms import CreateRecipeForm, RecipesSearchForm
from django.db.models import Q
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

@login_required
def home(request):
    return render(request, 'recipes/home.html')

def create_recipe(request):
    submitted = False 
    if request.method == "POST":
        form = CreateRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create_recipe?submitted=True')
    else: 
        form = CreateRecipeForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'recipes/create_recipe.html', {'form': form, 'submitted': submitted})

def search_bar(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        recipes = Recipe.objects.filter(name__icontains=searched)
        ingredients = Recipe.objects.filter(ingredients__icontains=searched)
        return render(request, 'recipes/search_bar.html', {'searched': searched, 'recipes': recipes, 'ingredients':ingredients})
    else:
        return render(request, 'recipes/search_bar.html', {})

def search_recipe(request):
    if request.method == 'GET':
        form = RecipesSearchForm(request.POST or None)  # Initialize an empty form for GET requests
        return render(request, 'recipes/recipe_search.html', {'form': form})
     
    form = RecipesSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    recipe_count = None
    ingredient_count = None

    if request.method =='POST':
        recipe_name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        chart_type = request.POST.get('chart_type')

        qs = Recipe.objects.all()
        
        if recipe_name:
            qs = qs.filter(name__icontains=recipe_name)#i ignores the case
        if ingredients:
            qs = qs.filter(ingredients__icontains=ingredients)
        

        if qs.exists():
            recipes_df=pd.DataFrame(qs.values())
            recipes_df['id'].apply(get_recipename_from_id)
            recipes_df=recipes_df.to_html()
            recipe = qs.first()
            recipe_id = recipe.id
            pic_url = recipe.pic.url
            initial_data = {
                'recipe_name': recipe_name, 
                'ingredients': ingredients, 
                'pic': pic_url,
                'chart_type': chart_type,
            }
            form = RecipesSearchForm(initial=initial_data)
       
        if len(qs) > 0:  # If data found
            # Get the count of all recipes and unique ingredients
            recipe_count = Recipe.objects.count()
            ingredient_count = len(set(ingredient.strip() for recipe in Recipe.objects.all() for ingredient in recipe.ingredients.split(', ')))

            # Call the get_recipe_ingredient_usage function to generate the chart
            chart = get_recipe_ingredient_usage(chart_type, recipe_id)

            # Get recipe data
            recipes_df = qs.values()

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
        'recipe_count': recipe_count,
        'ingredient_count': ingredient_count
    }
    return render(request, 'recipes/recipe_search.html', context)
