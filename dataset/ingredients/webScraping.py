import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get ingredient information from an ingredient theasuras, format, and expot to csv
# Creates csvs for all ingredients and liquids specifically (to be used to enure each soup has a liquid component)
# Each has two csvs, ingredient-root: maps each ingredient to its root ingredient, ingredient-alias: maps each ingredient to a list of aliases

# For All Ingredients

# set up arrays to store csv data
ingredient=[]
root=[]

# make call for ingredients
URL = "https://foodsubs.com/groups?name=&a=&page.number=0&page.size=4000&i=true"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")

# get ingredients
for a in soup.findAll('div', attrs={'class':'card-body d-flex flex-column h-100'}):
    name=a.find('a', href=True, attrs={'class':'card-title'})
    ingred = name.string.lower()
    ingredient.append(ingred)

    # make call for aliases
    str = name.string.lower().replace(" ", "-" ) # for url
    smallURL = "https://foodsubs.com/ingredients/" + str
    smallPage = requests.get(smallURL)
    ingr = BeautifulSoup(smallPage.text, "html.parser")

    # find aliases
    aliases=ingr.find('div', attrs={"ingredient-info-content"})
    if aliases != None: # if not empty
        ali = aliases.text.lower().split(", ")
        for nam in ali:
            ingredient.append(nam)
            root.append(ingred)
    else: # if empty
        ingredient.append(ingred)
        root.append(ingred)

print("All general ingredients scraped")

# convert to csv
df1 = pd.DataFrame({'ingredient':ingredient, 'root':root}) 
df1.to_csv('original/ingredient-root.csv', index=False, encoding='utf-8')

# For Liquids Only

# set up arrays to store csv data
ingredientL=[]
rootL=[]

# make call for ingredients
URLL = "https://foodsubs.com/groups/liquids?page.number=0&page.size=800&i=true"
pageL = requests.get(URLL)
soupL = BeautifulSoup(pageL.text, "html.parser")

# get ingredients
for a in soupL.findAll('div', attrs={'class':'card-body d-flex flex-column h-100'}):
    name=a.find('a', href=True, attrs={'class':'card-title'})
    ingred = name.string.lower()
    ingredientL.append(ingred)

    # make call for aliases
    str = name.string.lower().replace(" ", "-" ) # for url
    smallURL = "https://foodsubs.com/ingredients/" + str
    smallPage = requests.get(smallURL)
    ingr = BeautifulSoup(smallPage.text, "html.parser")

    # find aliases
    aliases=ingr.find('div', attrs={"ingredient-info-content"})
    if aliases != None: # if not empty

        ali = aliases.text.lower().split(", ")
        for nam in ali:
            ingredientL.append(nam)
            rootL.append(ingred)
    else: # if empty
        ingredientL.append(ingred)
        rootL.append(ingred)

print("All liquid ingredients scraped")

# convert to csv
df1L = pd.DataFrame({'ingredient':ingredientL, 'root':rootL}) 
df1L.to_csv('original/liquid-ingredient-root.csv', index=False, encoding='utf-8')

print("done")

# Helper function parses a string that contains ingredient information, returns an array of the ingredients
def stringParse(string):
    subString = string
    ingredients = []
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
    return ingredients

# Main:

# Read in modified ingredient list (hand modified)
df = pd.read_csv('modified/ingredient-root-mod.csv')

# Read df into arrays
ingredient = df['ingredient'].values.tolist()
root = df['root'].values.tolist()

# store final added ingredients to export to csv
newIngredient = dict()

# add ingredients from df into dict
# key represents [if the ingredient alias should be kept, root ingredient]
for i in range(len(ingredient)):
    newIngredient[ingredient[i]] = [True, root[i]]

print("Read in ingredient data from csv")

# make plural alias based in plural word rules
for i in range(len(ingredient)):
    if ingredient[i].endswith('on'):
        newStr = ingredient[i][:-2] + 'a'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('is'):
        newStr = ingredient[i][:-2] + 'es'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('us'):
        newStr = ingredient[i][:-2] + 'i'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('o'):
        newStr = ingredient[i] + 'es'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('y'):
        newStr = ingredient[i][:-1] + 'ies'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('f'):
        newStr = ingredient[i][:-1] + 'ves'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('fe'):
        newStr = ingredient[i][:-2] + 'ves'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('s'):
        newStr = ingredient[i] + 'ses'
        newIngredient[newStr] = [False, root[i]]
    if ingredient[i].endswith('z'):
        newStr = ingredient[i][:-2] + 'zes'
        newIngredient[newStr] = [False, root[i]]
    newStr = ingredient[i] + 'es'
    newIngredient[newStr] = [False, root[i]]
    newStr = ingredient[i] + 's'
    newIngredient[newStr] = [False, root[i]]
    
print("Made possible plural aliases")

# dict of all ingredients that are not already in the new ingredient list/ cannot be found
oddIngredients = dict()

# get recipe dataset
df = pd.read_csv('../recipes-dataset.csv')

print("Read in recipe data from csv")

# Greating the dicts from the database
# Reduces the number or plural aliases, if they are not an ingredient in the recipe database, they are not needed
for row in df.index:
    arr = stringParse(df['NER'][row])
    for el1 in range(1,len(arr) - 1):
        key = arr[el1].lower()
        if key in newIngredient:
            newIngredient[key][0] = True
        else:
            if key not in oddIngredients:
                oddIngredients[key] = None

print("Reduced possible ingredient aliases")

# ingredients not found in next phase
notFound = dict()

# split ingredients into words, sees if a substring of the ingredients of a consecutive set of words matches an ingredient
for ing in oddIngredients:
    plit = ing.split(" ")
    found = False
    for j in range(len(plit)):
        for i in range(j, len(plit) - j):
            if j == 0:
                stri = " ".join(plit[i:])
            else: 
                stri = " ".join(plit[i:-j])
            if stri in newIngredient:
                newIngredient[ing] = [True, newIngredient[stri][1]]
                found = True
                break
        if found: break
        for i in range(1, len(plit)-j):
            stri = " ".join(plit[j:-i])
            if stri in newIngredient:
                newIngredient[ing] = [True, newIngredient[stri][1]]
                found = True
                break
        if found: break
    if not found: 
        if ing in notFound:
            print(ing)
            notFound[ing] += 1
        else:
            notFound[ing] = 1

print("looked through odd ingredients")