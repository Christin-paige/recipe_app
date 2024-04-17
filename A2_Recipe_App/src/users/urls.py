from django.urls import path
from .views import home, records
app_name = 'users'

urlpatterns = [
   path('', home),
   path('users/', records)
]