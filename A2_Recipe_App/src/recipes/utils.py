from recipes.models import Recipe #connect parameters from recipe model
from io import BytesIO
from collections import Counter
import base64
import matplotlib.pyplot as plt
#define a function that takes the id

# Get all ingredients from the database
all_ingredients = [ingredient.strip() for recipe in Recipe.objects.all() for ingredient in recipe.ingredients.split(',')]

# Count the occurrences of each ingredient
ingredient_counts = Counter(all_ingredients)

# Extract ingredient names and counts
ingredients = list(ingredient_counts.keys())
recipe_counts = list(ingredient_counts.values())

def get_recipename_from_id(val):
    #this id is used to retrieve name from record
    recipename=Recipe.objects.get(id=val)
   
    #and returned back
    return recipename

def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #queryset of recipes
   #qs = data
   #filtered_qs = qs.filter(**kwargs)
   # Get all ingredients from the database
   all_ingredients = [ingredient.strip() for ingredient in data['ingredients']]

# Count the occurrences of each ingredient
   ingredient_counts = Counter(all_ingredients)

# Extract ingredient names and counts
   ingredients = list(ingredient_counts.keys())
   recipe_counts = list(ingredient_counts.values())
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')
   

   #specify figure size
   plt.figure(figsize=(6,3))

   #select chart_type based on user input from the form
   if chart_type == '#1':
      #plot bar chart between ?? on x-axis and ?? on y-axis
       plt.bar(ingredients, recipe_counts)
       plt.xlabel('Ingredients')
       plt.ylabel('Number of Recipes')
       plt.title('Number of Recipes Each Ingredient is In')
       plt.xticks(rotation=45)

       chart=get_graph()
       return chart


   elif chart_type == '#2':
       #generate pie chart based on the price.
       #The book titles are sent from the view as labels
       labels=kwargs.get('labels')
       plt.pie(data['cooking_time'], labels)

   elif chart_type == '#3':
       #plot line chart based on date on x-axis and price on y-axis
       plt.plot(data['name'], data['cooking_time'])
   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart = get_graph() 
   return chart  