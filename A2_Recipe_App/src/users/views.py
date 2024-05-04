from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'users/home.html')

#define function-based view - records(records()
def recipe_search(request):
   #do nothing, simply display page    
   return render(request, 'users/search_recipe.html')