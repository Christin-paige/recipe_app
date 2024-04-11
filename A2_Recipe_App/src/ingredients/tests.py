from django.test import TestCase
from .models import Ingredient

# Create your tests here.

class IngredientModelTest(TestCase):
    def setUpTestData():
        Ingredient.objects.create(name='Cinnamon', amount='1')

    def test_book_name(self):
        ingredient = Ingredient.objects.get(id=1)

        field_label = ingredient._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name')