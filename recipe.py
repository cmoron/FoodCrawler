# 27-12-15 Estelle Chauveau

#Recipe class, contains a list of ingredient (ingredients)
class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def prints(self):
        print(self.name)
        print(self.ingredients)
