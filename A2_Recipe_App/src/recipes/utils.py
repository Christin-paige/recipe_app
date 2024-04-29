from recipes.models import Recipe #connect parameters from recipe model
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
    #this id is used to retrieve name from record
    recipename=Recipe.objects.get(id=val)
    return recipename

def get_recipe_ingredient_usage(recipe_id, chart_type, **kwargs ):#retrieves chosen recipe
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    chosen_recipe_ingredients = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]#extracts ingredients
  # Count ingredient occurrences in all recipes (excluding the chosen one)
    all_ingredients = Recipe.objects.exclude(pk=recipe_id).values_list('ingredients', flat=True)
    ingredient_counts = Counter(ingredient for ingredients in all_ingredients for ingredient in ingredients.split(','))#counts ingredients in particular recipe
  # Filter ingredient counts based on chosen recipe ingredients
    filtered_counts = {ingredient: count for ingredient, count in ingredient_counts.items() if ingredient in chosen_recipe_ingredients}
  # Extract data for plotting
    ingredients = list(filtered_counts.keys())
    recipe_counts = list(filtered_counts.values())

   #select chart_type based on user input from the form
    if chart_type == '#1':
       plt.figure(figsize=(8,5))
       plt.bar(ingredients, recipe_counts)
       plt.xlabel('Ingredients')
       plt.ylabel('Number of Recipes')
       plt.title('Number of Recipes Each Ingredient is In')
       plt.xticks(rotation=45)

       buffer = BytesIO()#create a BytesIO buffer for the image
       plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
       plt.close()
       image_bytes = buffer.getValue()
       image_as_string = base64.b64encode(image_bytes).decode('utf-8')

       return image_as_string

    elif chart_type == '#2':
       #generate pie chart based on .
       #The book titles are sent from the view as labels
       labels=kwargs.get('labels')
       plt.pie(ingredients, recipe_counts, labels=labels)

    #elif chart_type == '#3':
       #plot line chart based on date on x-axis and price on y-axis
     #  plt.plot(data['name'], data['cooking_time'])
    #else:
     #  print ('unknown chart type')

   #specify layout details
    plt.tight_layout()

   #render the graph to file
    chart = get_graph() 
    return chart
 

