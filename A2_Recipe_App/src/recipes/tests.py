from django.test import TestCase
from .models import Recipe

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