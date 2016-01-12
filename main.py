# 27-12-15 Estelle Chauveau


from dbInterface import RandomFoodDataBase
from recipe import Recipe
from dataSourceInterface import DataSourceInterface

class main:
    def run(self):
        #DB is created
        random_food = RandomFoodDataBase()

        #The data is retrieved from the API. "q=q" mean the query is 'q', and "to=100" means the 100 first results
        #if they exist.
        dataInterface = DataSourceInterface("https://api.edamam.com/search?q=q&to=100")

        #Data is stored in an list of recipes objects.
        recipesList = dataInterface.getData();

        nbRecipes = len(recipesList)
        print(nbRecipes)
        for i in range(nbRecipes): #Eache recipe of the list is then added to the created db.
            recipe = recipesList[i]
            recipe.prints() #With a s because it was the best way to overload it nigga.
            random_food.addRecipe(recipe)
