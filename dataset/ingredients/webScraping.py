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