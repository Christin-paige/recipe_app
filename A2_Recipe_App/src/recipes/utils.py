from recipes.models import Recipe
from io import BytesIO
from collections import Counter
import base64
import matplotlib.pyplot as plt
from django.shortcuts import get_object_or_404

def get_graph():
    buffer = BytesIO()#create a BytesIO buffer for the image
    plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
    buffer.seek(0)#set cursor to the beginning of the stream
    image_png=buffer.getvalue()#retrieve the content of the file
    graph=base64.b64encode(image_png)#encode the bytes-like object
    graph=graph.decode('utf-8')#decode to get the string as output
    buffer.close()#free up the memory of buffer
    return graph#return the image/graph

def get_recipename_from_id(val):
    recipename=Recipe.objects.get(id=val)
    return recipename

def get_recipe_ingredient_usage(chart_type, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)#retrieve recipe
    #extract ingredients
    chosen_recipe_ingredients = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]

    all_ingredients = []
    
    for recipe in Recipe.objects.all():
        ingredients = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]
        all_ingredients.extend(ingredients)

    print(f"these ingredients {ingredients}")
    print(f"recipe: {recipe}")
    
    ingredient_counts = Counter(all_ingredients)#finds ingredient usage in all recipes

    filtered_counts = {ingredient: count for ingredient, count in ingredient_counts.items() if ingredient in chosen_recipe_ingredients}
    #keys = ingredient names, values = number of times each ingredient appears in other recipes

    ingredients = list(filtered_counts.keys())
    recipe_counts = list(filtered_counts.values())
   
 
   #select chart_type based on user input from the form
    if chart_type == '#1':
       plt.figure(figsize=(8,6))
       plt.bar(ingredients, recipe_counts)
       plt.xlabel('Ingredients')
       plt.ylabel('Number of Recipes')
       plt.title('Number of Recipes Containing Each Ingredient')
       plt.xticks(rotation=20)

       buffer = BytesIO()#create a BytesIO buffer for the image
       plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
       plt.close()
       image_bytes = buffer.getvalue()
       image_as_string = base64.b64encode(image_bytes).decode('utf-8')
       return image_as_string

    elif chart_type == '#2':
       #generate pie chart based
       plt.figure(figsize=(8,8))
       plt.pie(recipe_counts, labels=ingredients, autopct='%1.1f%%')
       plt.title("Percentage of Total Recipes Containing Each Ingredient")

       buffer = BytesIO()#create a BytesIO buffer for the image
       plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
       plt.close()
       image_bytes = buffer.getvalue()
       image_as_string = base64.b64encode(image_bytes).decode('utf-8')
       return image_as_string
    
    elif chart_type == '#3':
       #generate line chart based
       plt.plot(ingredients, recipe_counts)
       plt.title("Number of Recipes Containing Each Ingredient")
       plt.xlabel('Ingredients')
       plt.ylabel('Number of Recipes')

       buffer = BytesIO()#create a BytesIO buffer for the image
       plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
       plt.close()
       image_bytes = buffer.getvalue()
       image_as_string = base64.b64encode(image_bytes).decode('utf-8')
       return image_as_string
 
    else:
        return None
 

