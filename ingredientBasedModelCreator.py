# Dependancies
import pandas as pd
import numpy as np

# Comparison class that stores information comparing two ingredients
#   cohesion: how many recepies have this ingredient with the other ingredient
#               (how well these ingredients work together)
#   ordering: how often this ingredient is listed before another ingredient
#               (if negative, this ingredient is usually listed before, if positive, this ingredient is usually listed after)
class Comparison:
    def __init__(self, name):
        self.name = name
        self.cohesion = 0
        self.ordering = 0

    # Update ordering value
    def updateOrdering(self, order):
        self.ordering += order

    # Update cohesion value
    def updateCohesion(self, cohesion):
        self.cohesion += cohesion

# Stores information on ingredients
#   name: name of the ingredient
#   numRecipe: number of recepies that has this ingredient
#   parents: dict of igredients that are listed right before the ingredient and how often it is listed right before
#   children: dict of igredients that are listed right after the ingredient and how often it is listed right after
#   cohesion: dict of all ingredients that this ingredient is in the same recipe in and information about that ingredient
class Ingredient:
    def __init__(self, name):
        self.name = name
        self.numRecipe = 1
        self.parents = dict()
        self.children = dict()
        self.cohesion = dict()

    # Incriment the number of recipes this ingredient is in
    def incrimentNumRecipe(self):
        self.numRecipe += 1

    # Adds a parent to parents dict, or update a node
    def addParent(self, ingredient):
        if ingredient in self.parents:
            self.parents[ingredient] += 1
        else:
            self.parents[ingredient] = 1

    # Adds a child to children dict, or update a node
    def addChild(self, ingredient):
        if ingredient in self.children:
            self.children[ingredient] += 1
        else:
            self.children[ingredient] = 1

    # Adds or updates ingredient information for cohesion dict
    def addIngredient(self, ingredient, ordering):
        if ingredient in self.cohesion:
            self.cohesion[ingredient].updateCohesion(1)
            self.cohesion[ingredient].updateOrdering(ordering)
        else:
            cohesion = Comparison(ingredient)
            cohesion.updateCohesion(1)
            cohesion.updateOrdering(ordering)
            self.cohesion[ingredient] = cohesion

    # Prints information on the ingredient
    def printInfo(self):
        print("\nname: " + self.name)
        print("number of recipes: " + str(self.numRecipe))
        print("parent ingredients: ")
        for key in self.parents:
            print("\t" + key + " : " + str(self.parents[key]))
        print("child ingredients: ")
        for key in self.children:
            print("\t" + key + " : " + str(self.children[key]))
        print("cohesion ingredients: ")
        for key in self.cohesion:
            print("\t" + key + " cohesion : " + str(self.cohesion[key].cohesion) + " ordering : " + str(self.cohesion[key].ordering))


# Parses a string that contains ingredient information, returns an array of the ingredients
def stringParse(string):
    subString = string
    ingredients = []
    ingredients.append('nil')
    startIndex = subString.find('"')
    while startIndex != -1:
        endIndex = subString.find('"', startIndex + 1)
        if endIndex == -1:
            break
        startIndex += 1
        if startIndex >= endIndex:
            break   
        ingredients.append(subString[startIndex: endIndex])
        subString = subString[endIndex + 1:]
        startIndex = subString.find('"')
    ingredients.append('nil')
    return ingredients

# Main

# database we use for recipes
dfr = pd.read_csv('dataset/recipes-dataset.csv')

# database we use for ingredients
dfi = pd.read_csv('dataset/ingredients/modified/ingredient-root-was-modified-wliquid.csv')

# create a dict for possible ingredients
possibleIngredients = dict()

# fill possible ingredient dict
for i in range(len(dfi)):
    possibleIngredients[dfi["ingredient"][i]] = dfi["root"][i]

# dicts for our information structures (to be exported to csv)
ingredients = dict()
soupIngredients = dict()

# Greating the dicts from the database
for row in dfr.index:
    arr = stringParse(dfr['NER'][row])
    # for the soup ingredient dict
    if 'soup' in dfr['title'][row] or 'broth' in dfr['title'][row] or 'stock' in dfr['title'][row] or 'stew' in dfr['title'][row] or 'bisque' in dfr['title'][row] or 'chowder' in dfr['title'][row] or 'goulash' in dfr['title'][row] or 'bouillon' in dfr['title'][row] or 'consomme' in dfr['title'][row] or 'cream of' in dfr['title'][row] or 'gazpacho' in dfr['title'][row] or 'minestrone' in dfr['title'][row]: 
        for el1 in range(1,len(arr) - 1):
            key = arr[el1].lower()
            if key in possibleIngredients:
                root = possibleIngredients[key]
                if root in soupIngredients:
                    soupIngredients[root].incrimentNumRecipe()
                else:
                    soupIngredients[root] = Ingredient(root)
                for el2 in range(len(arr)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        if valRoot == root:
                            continue
                        soupIngredients[root].addIngredient(valRoot, el2 - el1)
                for el2 in reversed(range(el1)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        soupIngredients[root].addParent(valRoot)
                        break
                for el2 in range(el1 + 1, len(arr)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        soupIngredients[root].addChild(valRoot)
                        break
            # else: print(key)
    # for the general ingredient dict
    for el1 in range(1,len(arr) - 1):
            key = arr[el1].lower()
            if key in possibleIngredients:
                root = possibleIngredients[key]
                if root in ingredients:
                    ingredients[root].incrimentNumRecipe()
                else:
                    ingredients[root] = Ingredient(root)
                for el2 in range(len(arr)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        if valRoot == root:
                            continue
                        ingredients[root].addIngredient(valRoot, el2 - el1)
                        if el1 == el2 + 1:
                            ingredients[root].addParent(valRoot)
                        elif el1 == el2 - 1:
                            ingredients[root].addChild(valRoot)
                for el2 in reversed(range(el1)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        ingredients[root].addParent(valRoot)
                        break
                for el2 in range(el1 + 1, len(arr)):
                    val = arr[el2].lower()
                    if val in possibleIngredients:
                        valRoot = possibleIngredients[val]
                        ingredients[root].addChild(valRoot)
                        break

# format ingredients

# for all ingredients
names = []
numRecipe = []
parents = []
children = []
cohesion = []

for ing in ingredients:
    if not ing in possibleIngredients:
        print(ing)
    ingredient = ingredients[ing]
    names.append(ingredient.name)
    numRecipe.append(ingredient.numRecipe)
    parentStr = ''
    childrenStr = ''
    cohesionStr = ''
    orderStr = ''
    for par in ingredient.parents:
        if ingredient.parents[par] <= 0: print(par + " in " + ingredient.name)
        parentStr += str(par) + ":" + str(ingredient.parents[par]) + ","
    parents.append(parentStr[:-1])
    for child in ingredient.children:
        if ingredient.children[child] <= 0: print(child + " in " + ingredient.name)
        childrenStr += str(child) + ":" + str(ingredient.children[child]) + ","
    children.append(childrenStr[:-1])
    for co in ingredient.cohesion:
        cohesionStr += str(ingredient.cohesion[co].name) + ":" + str(ingredient.cohesion[co].cohesion) + ":" + str(ingredient.cohesion[co].ordering) + ","
    cohesion.append(cohesionStr[:-1])

# for soup ingredients  
soupNames = []
soupNumRecipe = []
soupParents = []
soupChildren = []
soupCohesion = []

for ing in soupIngredients:
    if not ing in possibleIngredients:
        print(ing)
    ingredient = soupIngredients[ing]
    soupNames.append(ingredient.name)
    soupNumRecipe.append(ingredient.numRecipe)
    parentStr = ''
    childrenStr = ''
    cohesionStr = ''
    orderStr = ''
    for par in ingredient.parents:
        if ingredient.parents[par] <= 0: print(par + " in " + ingredient.name)
        parentStr += str(par) + ":" + str(ingredient.parents[par]) + ","
    soupParents.append(parentStr[:-1])
    for child in ingredient.children:
        if ingredient.children[child] <= 0: print(child + " in " + ingredient.name)
        childrenStr += str(child) + ":" + str(ingredient.children[child]) + ","
    soupChildren.append(childrenStr[:-1])
    for co in ingredient.cohesion:
        cohesionStr += str(ingredient.cohesion[co].name) + ":" + str(ingredient.cohesion[co].cohesion) + ":" + str(ingredient.cohesion[co].ordering) + ","
    soupCohesion.append(cohesionStr[:-1])
    
# to csv
dfL = pd.DataFrame({'name':names, 'num':numRecipe,'parents':parents,'children':children,'cohesion':cohesion}) 
dfL.to_csv('model/ing-based-ingredient-model.csv', index=False, encoding='utf-8')
dfL = pd.DataFrame({'name':soupNames, 'num':soupNumRecipe,'parents':soupParents,'children':soupChildren,'cohesion':soupCohesion}) 
dfL.to_csv('model/ing-based-soup-ingredient-model.csv', index=False, encoding='utf-8')