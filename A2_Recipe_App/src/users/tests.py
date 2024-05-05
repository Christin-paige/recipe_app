from django.test import TestCase
from .models import User

# Create your tests here.
class MyTestClass(TestCase):
    def setUpTestData():
        User.objects.create(name="Wilbur")

    def test_user_name(self):
        user=User.objects.get(id=1)

        field_label = user._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name')

    def test_user_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)


