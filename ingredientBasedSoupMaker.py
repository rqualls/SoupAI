# Dependancies
import pandas as pd
import numpy as np
import random
from enum import Enum
import functools

# Constants
REJECT_VALUE = .05
MAX_INGREDIENTS = 15
MAX_LISTED_INGREDIENTS = 5

# Classification enum, what type of ingredient based on if it were
#   original: originally specified by the user
#   child: the child of a previous ingredient
#   parent: the parent of a previous ingredient
class Classification(Enum):
    original = 1
    child = 2
    parent = 3

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
    def addIngredient(self, ingredient, cohesion, ordering):
        if ingredient in self.cohesion:
            self.cohesion[ingredient].updateCohesion(cohesion)
            self.cohesion[ingredient].updateOrdering(ordering)
        else:
            cohesionV = Comparison(ingredient)
            cohesionV.updateCohesion(cohesion)
            cohesionV.updateOrdering(ordering)
            self.cohesion[ingredient] = cohesionV

    # Check compadibility of two ingredients
    def checkCompadibility(self, ingredient):
        if ingredient in self.cohesion:
            #print(self.name + " compatibility with " + ingredient + " is " + str(self.cohesion[ingredient].cohesion / self.numRecipe))
            if self.cohesion[ingredient].cohesion / self.numRecipe > REJECT_VALUE:
                return True
        #print(self.name + " does not have high enough compatibility with " + ingredient)
        return False
    
    # Check order of two ingredients
    def checkIngredient(self, ingredient):
        if ingredient in self.cohesion:
            return self.cohesion[ingredient].ordering
        return 0

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

# Custom compare function to order final ingredients
def compare(x, y):
    if x in soupIngredients and y in soupIngredients:
        return soupIngredients[x].checkCompadibility(y) - soupIngredients[y].checkCompadibility(x)
    if x in ingredients and y in ingredients:
        return (ingredients[x].checkCompadibility(y) - ingredients[y].checkCompadibility(x))
    return 0

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

# Chooses the next ingredient based on current ingredient
#   parent: bool of if we want to choose an element from the child or parent list
def chooseNext(ingredient, parent):
    if ingredient in soupIngredients:
        if parent:
            choice = random.choices(list(soupIngredients[ingredient].parents.keys()), weights=list(soupIngredients[ingredient].parents.values()), k=1)
            return choice[0]
        else:
            choice = random.choices(list(soupIngredients[ingredient].children.keys()), weights=list(soupIngredients[ingredient].children.values()), k=1)
            return choice[0]
    elif ingredient in ingredients:
        if parent:
            choice = random.choices(list(ingredients[ingredient].parents.keys()), weights=list(ingredients[ingredient].parents.values()), k=1)
            return choice[0]
        else:
            choice = random.choices(list(ingredients[ingredient].children.keys()), weights=list(ingredients[ingredient].children.values()), k=1)
            return choice[0]
    else:
        return "nil"
    
# Check given list for compadibility of given ingredient with ingredients only in the list
#   Returns a bool
def checkList(ingredient, ingredientList):
    for ing in ingredientList:
        if ing in soupIngredients and ingredient in soupIngredients:
            if soupIngredients[ing].checkCompadibility(ingredient) or soupIngredients[ingredient].checkCompadibility(ing):
                continue
           
        if ing in ingredients and ingredient in ingredients:
            if not(ingredients[ing].checkCompadibility(ingredient) or ingredients[ingredient].checkCompadibility(ing)):
                return False
    return True

# Fill ingredient models from csv
#   ingredientsDF: dataframe that stores ingredient model
#   ingredientDict: dict that stores the model information
def fillModel(ingredientsDF, ingredientDict):
    for i in range(len(ingredientsDF)):
        name = ingredientsDF['name'][i]
        ingredientDict[name] = Ingredient(name)
        ingredientDict[name].numRecipe = ingredientsDF['num'][i]
        if type(ingredientsDF['parents'][i]) == str:
            parents = ingredientsDF['parents'][i].split(',')
            for parent in parents:
                split = parent.split(':')
                if len(split) == 2:
                    ingredientDict[name].parents[split[0]] = int(split[1])
        else: print(name + " has no parents")
        if type(ingredientsDF['children'][i]) == str:
            children = ingredientsDF['children'][i].split(',')
            for child in children:
                split = child.split(':')
                if len(split) == 2:
                    ingredientDict[name].children[split[0]] = int(split[1])
        else: print(name + " has no children")
        if type(ingredientsDF['cohesion'][i]) == str:
            cohesion = ingredientsDF['cohesion'][i].split(',')
            for co in cohesion:
                split = co.split(':')
                if len(split) == 3:
                    ingredientDict[name].addIngredient(split[0], int(split[1]), int(split[2]))

# Generates ingredients for soup given an ingredient list
#   ingredientList: dict of ingredients given
def generateIngredients(ingredientList):
    hasLiquid = False

    for ing in ingredientList:
        if liquidIngredients[ing]:
            print(ing)
            hasLiquid = True

    while(True):
        newIngredients = dict()
        for ing in ingredientList:
            if ingredientList[ing][0]:
                if ingredientList[ing][1] == Classification.original or ingredientList[ing][1] == Classification.child:
                    coun = 0
                    while(coun < MAX_INGREDIENTS - len(ingredientList) - len(newIngredients)):
                        coun += 1
                        newIng = chooseNext(ing, False)
                        if newIng == "nil":
                            break
                        if checkList(newIng, ingredientList) and checkList(newIng, newIngredients):
                            newIngredients[newIng] = (True, Classification.child)
                            if liquidIngredients[newIng]:
                                hasLiquid = True
                            break
                if ingredientList[ing][1] == Classification.original or ingredientList[ing][1] == Classification.parent:
                    coun = 0
                    while(coun < MAX_INGREDIENTS - len(ingredientList) - len(newIngredients)):
                        coun += 1
                        newIng = chooseNext(ing, True)
                        if newIng == "nil":
                            break
                        if checkList(newIng, ingredientList) and checkList(newIng, newIngredients):
                            newIngredients[newIng] = (True, Classification.parent)
                            if liquidIngredients[newIng]:
                                hasLiquid = True
                            break
                ingredientList[ing] = (False, Classification.original) # the classification does not matter if it is false
        if len(newIngredients) != 0:
            ingredientList.update(newIngredients)
        elif not hasLiquid:
            # go crazy and try to get a liquid
            for _ in range(50):
                for ing in ingredientList:
                    newIng = chooseNext(ing, False)
                    if liquidIngredients[newIng]:
                        if checkList(newIng, ingredientList):
                            newIngredients[newIng] = (True, Classification.original)
                            hasLiquid = True
                            break 
                if hasLiquid:
                    break
            if hasLiquid:
                    break
            else:
                print("We could not make a propper soup based on the specified ingredients")  
                break 
        else:
            break
    # order ingredients using a sorting algorithm
    sortedIngredients = sorted(list(ingredientList.keys()), key=functools.cmp_to_key(compare))
    return sortedIngredients

# Main

# database we use for ingredients
dfi = pd.read_csv('dataset/ingredients/modified/ingredient-root-was-modified-wliquid.csv')

# create a dict for possible ingredients
possibleIngredients = dict()
liquidIngredients = dict()

# fill possible ingredient dict
for i in range(len(dfi)):
    possibleIngredients[dfi["ingredient"][i]] = dfi["root"][i]
    liquidIngredients[dfi["ingredient"][i]] = dfi["liquid"][i]

# ingredient models
ingredientDF = pd.read_csv('model/ing-based-ingredient-model.csv')
soupIngredientDF = pd.read_csv('model/ing-based-soup-ingredient-model.csv')

ingredients = dict()
soupIngredients = dict()

# fill regular and soup ingredient models from csv
fillModel(ingredientDF, ingredients)
fillModel(soupIngredientDF, soupIngredients)

# start output
print("Welcome to the soup generator")
while(True):
    print("Please input 1 to " + str(MAX_LISTED_INGREDIENTS) + " ingredients to make soup and we will provide you with the rest of the ingredients")
    print("Type 'quit' to quit")
    print("Type 'done' after you have entered your last ingredient")
    ingredientList = dict()
    count = 0
    usrInput = ''
    while(count < MAX_LISTED_INGREDIENTS):
        usrInput = input("Input an ingredient: ")
        usrInput = usrInput.lower()
        if usrInput == "quit":
            break
        if usrInput == "done":
            if len(ingredientList) == 0:
                print("You need at least 1 ingredient")
                continue
            break
        if usrInput in ingredientList:
            print("You have already added this ingredient silly!")
            continue
        if usrInput not in possibleIngredients:
            print("We did not find this ingredient in our list, try a different one")
            continue
        root = possibleIngredients[usrInput]
        ingredientList[root] = (True, Classification.original)
        count += 1
        print("Your input ingredients include: ")
        for ing in ingredientList:
            print(ing, end=' ')
        print("\n")
    if usrInput == "quit":
        break

    # order ingredients using a sorting algorithm
    sortedIngredients = generateIngredients(ingredientList)

    # print final ingredients
    print("Your ingredients in your soup are: ")
    for ing in sortedIngredients:
        print("\t" + ing)
