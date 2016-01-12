#!/usr/bin/python
# coding: utf8
# 27-12-15 Estelle Chauveau
# Interface with the mySQL database

from recipe import Recipe
import _mysql #For the database connexion;
import MySQLdb #For reading data from the database (fetchall() method).
import _mysql_exceptions #For catchin gmysql exception (in queries)

db =  _mysql.connect()
dbForReadingData = MySQLdb.connect()
cursor = dbForReadingData.cursor()

#This method return the primary key of an ingredient in the ingredients table
def getKeyIngredient(ingredient):
    dbForReadingData.commit()
    cursor = dbForReadingData.cursor()
    sql1 = "USE random_food"
    sql2 = "select Ingredient_Id from ingredients where Name='%s';"
    cursor.execute(sql1)
    cursor.execute(sql2%ingredient)
    results = cursor.fetchall()
    if len(results)>0:
        if len(results[0])>0:
            result = (results[0][0])
            return result;
        else:
            print("The ingredient seems not to be in the data base")
    else:
        print("The ingredient seems not to be in the data base")



#This method return the primary key of an recipe in the recipes table
def getKeyRecipe(recipe):
    dbForReadingData.commit()
    cursor = dbForReadingData.cursor()
    sql1 = "USE random_food"
    sql2 = "select Recipe_Id from recipes where Name='%s';"
    cursor.execute(sql1)
    cursor.execute(sql2%recipe)
    results = cursor.fetchall()
    if len(results)>0:
        if len(results[0])>0:
            result = (results[0][0])
            return result;
        else:
            print("The recipe seems not to be in the data base")
    else:
        print("The recipe seems not to be in the data base")

#The random_food database manager
class RandomFoodDataBase: 

    #constructor (builds 3 empty tables)
    #Warning: an error is raised if the tables already exists. The initDB.py script can be used in this case.
    def __init__(self):
        db.query("CREATE DATABASE random_food")
        db.query("USE random_food;") 
        db.query("""CREATE TABLE recipes(Recipe_Id INT AUTO_INCREMENT PRIMARY KEY, Name varchar(300) UNIQUE NOT NULL)""");
        db.query("""CREATE TABLE ingredients(Ingredient_Id INT AUTO_INCREMENT PRIMARY KEY, Name varchar(50) UNIQUE NOT NULL);""")
        db.query("""CREATE TABLE recipes_ingredients (R_Id INT, I_Id INT, PRIMARY KEY (R_Id, I_Id));""")
        print("random_food database created")

    #Method for adding a recipe. Take a Recipe object in argument.
    def addRecipe(self, recipe):
        recipeName = recipe.name.replace(u"'",u"\\'")#the apostrophe raises error in mysql syntax.
        #TODO find a way to keep the correct name of the recipe...
        recipeName = recipeName.replace(u"é",u"e")#The accent raises error in mysql syntax.
        try:
            db.query(u"""INSERT INTO recipes(Name) VALUES ('%s');"""%(recipeName))
        except :
            pass
        print("New recipe added to the database:")
        nbIngredients = len(recipe.ingredients)
        recipe_id = getKeyRecipe(recipeName)
        print("recipe id:"+str(recipe_id))
        #Iteration on all ingredients to add them in the db.
        for i in range(nbIngredients) :
            try:
                ingredientName = recipe.ingredients[i];
                db.query("""INSERT INTO ingredients(Name) VALUES ('%s');"""%(ingredientName))
            except  _mysql_exceptions.IntegrityError:
                pass
            print("ingredient ajoute: "+str(ingredientName))
            db.commit()
            ingredient_id = getKeyIngredient(ingredientName)
            try:
                #Complete the junction table (matches recipe with ingredient key biatch)
                db.query("INSERT INTO recipes_ingredients VALUES (%d,%d)"%(recipe_id,ingredient_id))
            except _mysql_exceptions.IntegrityError:
                pass

    def closeDB():
        db.close()



