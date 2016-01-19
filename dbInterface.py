#!/usr/bin/python
# coding: utf8
# 19-01-16 EMaulandi
#TODO : stocker nom DB ailleurs que en dur !
# Interface with the mySQL database

from recipe import Recipe
import _mysql #For the database connexion;
import MySQLdb #For reading data from the database (fetchall() method).
import _mysql_exceptions #For catchin gmysql exception (in queries)

#SET YOUR DATABASE NAME HERE
#database_name = 

## PLEASE ADD YOUR DB CREDENTIALS BELOW
#db =  _mysql.connect('localhost', your user here, your user secret here, database_name)
#dbForReadingData = MySQLdb.connect('localhost', your user here, your user secret here, database_name)
db =  _mysql.connect()
dbForReadingData = MySQLdb.connect()
cursor = dbForReadingData.cursor()

##Database fields
recipe_table = 'recipes'
recipe_id = 'Recipe_Id'
recipe_name = 'Name'

ingredient_table = 'ingredients'
ingredient_id = 'Ingredient_Id'
ingredient_name = 'Name'

#This method return the primary key of an ingredient in the ingredients table
def getKeyIngredient(ingredient):
    dbForReadingData.commit()
    cursor = dbForReadingData.cursor()
    sql1 = "USE %s;"%(database_name)
    sql2 = "select %s from %s where %s='%s';"%(ingredient_id,ingredient_table,ingredient_name,ingredient)
    cursor.execute(sql1)
    cursor.execute(sql2)
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
    sql1 = "USE %s;"%(database_name)
    sql2 = "select %s from %s where %s='%s';"%(recipe_id,recipe_table,recipe_name,recipe)
    cursor.execute(sql1)
    cursor.execute(sql2)
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
	print("enter")
	try:
	## No DB creation for now, should be already created
		# db.query("CREATE DATABASE random_food")
		#  db.query("USE random_food;") 
		# db.query("""CREATE TABLE recipes(Recipe_Id INT AUTO_INCREMENT PRIMARY KEY, Name varchar(300) UNIQUE NOT NULL)""");
		# db.query("""CREATE TABLE ingredients(Ingredient_Id INT AUTO_INCREMENT PRIMARY KEY, Name varchar(50) UNIQUE NOT NULL);""")
		# db.query("""CREATE TABLE recipes_ingredients (R_Id INT, I_Id INT, PRIMARY KEY (R_Id, I_Id));""")
		# print("random_food database created")

		## Checking the version for test purpose
		cursor = dbForReadingData.cursor()
	    	cursor.execute("SELECT VERSION()")
	    	ver = cursor.fetchone()
		print "Database version : %s " % ver
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])


    #Method for adding a recipe. Take a Recipe object in argument.
    def addRecipe(self, recipe):
        recipeName = recipe.name.replace(u"'",u"\\'")#the apostrophe raises error in mysql syntax.
        #TODO find a way to keep the correct name of the recipe...
        recipeName = recipeName.replace(u"é",u"e")#The accent raises error in mysql syntax.
        try:
		#test si recette existe dejà
		cursor = dbForReadingData.cursor()
		cursor.execute("SELECT * FROM %s WHERE %s = '%s';"%(recipe_table,recipe_name,recipeName))
		exist = cursor.fetchone()
		if exist == None:
 
            		db.query(u"""INSERT INTO %s(%s) VALUES ('%s');"""%(recipe_table,recipe_name,recipeName))
			print("New recipe added to the database:")
			nbIngredients = len(recipe.ingredients)
			recipe_id = getKeyRecipe(recipeName)
			print("recipe id:"+str(recipe_id))
			#Iteration on all ingredients to add them in the db.
			for i in range(nbIngredients) :
			    try:
				ingredientName = recipe.ingredients[i];
				#test si ingredient existe dejà
				cursor = dbForReadingData.cursor()
				cursor.execute("SELECT * FROM %s WHERE %s = '%s';"%(ingredient_table,ingredient_name,ingredientName))
				exist = cursor.fetchone()
				if exist == None:
					db.query("""INSERT INTO %s(%s) VALUES ('%s');"""%(ingredient_table,ingredient_name,ingredientName))
					print("ingredient ajoute: "+str(ingredientName))
				else:
					print("ingredient deja existant: "+str(ingredientName))
			    except  _mysql_exceptions.IntegrityError:
				pass
			    
			    db.commit()
			    ingredient_id = getKeyIngredient(ingredientName)
			    try:
				#Complete the junction table (matches recipe with ingredient key biatch)
				db.query("INSERT INTO recipes_ingredients VALUES (%d,%d)"%(recipe_id,ingredient_id))
			    except _mysql_exceptions.IntegrityError:
				pass
		else:
			print("Recipe Already exists")
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])


    def closeDB():
	db.close()



