from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name=models.CharField(max_length=120)
    amount=models.FloatField(help_text='in cups, tbs, tsp')

    def __str__(self):
        return str(self.name)