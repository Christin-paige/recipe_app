from django.urls import path
from .views import home, recipe_search
app_name = 'users'

urlpatterns = [
   path('', home),
   path('users/', recipe_search)
]