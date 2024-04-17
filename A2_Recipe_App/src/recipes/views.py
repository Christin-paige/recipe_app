from django.shortcuts import render
from django.views.generic import ListView, DetailView  #to display lists
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/main.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
# Create your views here.
def home(request):
    return render(request, 'recipes/home.html')






