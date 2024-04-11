from django.db import models

# Create your models here.
class Recipe(models.Model):
    name=models.CharField(max_length=120)
    ingredients=models.CharField(max_length=250)
    cooking_time=models.FloatField(help_text='in minutes')

    def __str__(self):
        return str(self.name)
