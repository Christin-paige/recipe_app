from django.db import models
from django.shortcuts import reverse


# Create your models here.


class Recipe(models.Model):
    name=models.CharField(max_length=120)
    ingredients=models.CharField(max_length=250)
    cooking_time=models.FloatField(help_text='in minutes')
    pic = models.ImageField(upload_to='recipes/', default='no_picture.jpg')

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
       return reverse ('recipes:detail', kwargs={'pk': self.pk})
