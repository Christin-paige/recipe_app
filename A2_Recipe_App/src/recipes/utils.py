from recipes.models import Recipe #connect parameters from recipe model
from io import BytesIO
from collections import Counter
import base64
import matplotlib.pyplot as plt



def get_recipename_from_id(val):
    #this id is used to retrieve name from record
    recipename=Recipe.objects.get(id=val)
   
    #and returned back
    return recipename

def get_graph():
    buffer = BytesIO()#create a BytesIO buffer for the image
    plt.savefig(buffer, format='png')#create a plot with a bytesIO object as a file-like object. Set format to png
    buffer.seek(0)#set cursor to the beginning of the stream
    image_png=buffer.getvalue()#retrieve the content of the file
    graph=base64.b64encode(image_png)#encode the bytes-like object
    graph=graph.decode('utf-8')#decode to get the string as output
    buffer.close()#free up the memory of buffer
    return graph#return the image/graph
   

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #queryset of recipes
   #qs = data
   #filtered_qs = qs.filter(**kwargs)
   # Get all ingredients from the database
   all_ingredients = [ingredient.strip() for recipe in Recipe.objects.all() for ingredient in recipe.ingredients.split(',')]
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