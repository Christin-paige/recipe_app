from django.test import TestCase
from .models import Recipe
from .forms import RecipesSearchForm
from .forms import CreateRecipeForm
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(name="granola", ingredients="oats", cooking_time="20")

    def test_recipe(self):
        recipe = Recipe.objects.get(id=1)

        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        #get absolute url, should take you to the details page of the first recipe
        #load the url of the first recipe
        self.assertEqual(recipe.get_absolute_url(), '/list/1')

class RecipeFormTest(TestCase):

    def setUp(self):
        pass
    
    def test_recipe_form_valid(self):
        form_data = {'recipe_name' : 'name', 'ingredients': 'Ingredient', 'chart_type': '#1'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_recipe_form(self):
        form_data = {'recipe_name' : 'name', 'ingredients' : 'ingredients', 'cooking_time' : 'cooking_time', 'pic' : 'pic'}
        form = CreateRecipeForm(data=form_data)
        self.assertTrue(form.is_valid)

class LoginTest(TestCase): 
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_successful_login(self):
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:home'))
        self.assertTrue(self.client.login(username='testuser', password='password'))
