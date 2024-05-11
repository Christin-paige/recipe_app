from django.urls import path
from .views import home, RecipeListView, RecipeDetailView
from . import views

app_name = 'recipes' 

urlpatterns = [
   path('', home, name='home'),
   path('list/', RecipeListView.as_view(), name='list'),
   path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
   path('create_recipe', views.create_recipe, name='create_recipe'),
   path('search_recipe', views.search_recipe, name='search_recipe'),
   path('search_bar', views.search_bar, name='search_bar'),
  
]
