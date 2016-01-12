#!/usr/bin/python
# 27-12-15 Estelle Chauveau

import _mysql

db = _mysql.connect()        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need


#db.query("CREATE DATABASE random_food")
#db.query("USE random_food;") 

db.query("DROP DATABASE random_food")

