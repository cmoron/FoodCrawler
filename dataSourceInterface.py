# -*- coding: utf-8 -*-
# 27-12-15 Estelle Chauveau
#Interface with the Edamam API

from recipe import Recipe #The DataSourceInterface object return a list of Recipe objects.
import urllib2 #For API data retrieving.
import json #For data reading.

'''
#This commented part allows to test quickly by using a recipe stored in a local file (instead of working with the API)
mon_fichier = open("url.txt", "r")
texte = mon_fichier.read()
mon_fichier.close()
'''

class DataSourceInterface:

    #Constructor (the data is retrieved from the API).
    def __init__(self, request):
        self.recipesListOut = []
        self.request = request
        try:
            url=urllib2.urlopen(request)
        except:
            print("Bad url (or rquest), the data cannot be retrieved from Edamam API")
        text = url.read()
        io = json.loads(text)
        recipeList = io['hits']#Access to the list containing all the recipes.
        nbRecipes = len(recipeList)
        #Iteration on the recipe list.
        for i in range(nbRecipes):
            recipe = recipeList[i]['recipe']
            recipeName = recipe['label']
            ingredientsList = recipe['ingredients']
            nbIngredients =len(ingredientsList)
            ingredientsListOutput = []
            #iteration on the ingredient list.
            for j in range(nbIngredients):
                ingredient = ingredientsList[j]['food']
                ingredientsListOutput.append(ingredient)
            recipeObject = Recipe(recipeName,ingredientsListOutput)
            self.recipesListOut.append(recipeObject)


    #Data getter, return a list of Recipe objects.
    def getData(self):
        return self.recipesListOut


