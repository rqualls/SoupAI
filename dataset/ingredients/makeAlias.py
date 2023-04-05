import pandas as pd
import copy
import enchant

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

# The following commented out code attempts to reduce the number of unmatched ingredients in the recepies
# however many incorrectly assumes matches, so preserve the correction of the matches, we do not use it
# balance between amount of data and correctness of data used

## Looks through normal ingredients (that in newIngredients), splits into substrings, and determines if
## a consecutive set of words matches the ingredients in notFound

# newNewIngredient = copy.deepcopy(newIngredient)
# # notFoun = copy.deepcopy(notFound)
# empty = False

# while not empty:
#     oldIngs = copy.deepcopy(newNewIngredient)
#     newNewIngredient.clear()
#     for ing in oldIngs:
#         plit = ing.split(" ")
#         found = False
#         for j in range(len(plit)):
#             for i in range(j, len(plit) - j):
#                 if j == 0:
#                     stri = " ".join(plit[i:])
#                 else: 
#                     stri = " ".join(plit[i:-j])
#                 if stri in notFound and notFound[stri] > 0:
#                     newNewIngredient[stri] = [True, newIngredient[ing][1]]
#                     found = True
#                     notFound[stri] = 0
#                     break
#             if found: break
#             for i in range(1, len(plit)-j):
#                 stri = " ".join(plit[j:-i])
#                 if stri in notFound and notFound[stri] > 0:
#                     newNewIngredient[stri] = [True, newIngredient[ing][1]]
#                     found = True
#                     notFound[stri] = 0
#                     break
#             if found: break
#         # if not found: 
#         #     if ing in notFoun:
#         #         notFoun[ing] += 1
#         #     else:
#         #         notFoun[ing] = 1
#     empty = True
#     newIngredient.update(newNewIngredient)
#     if len(newNewIngredient) == 0:
#         empty = True
#     else: 
#         print("num of new ing: " + str(len(newNewIngredient)))
#         # notFoun.clear()

# print("looked through normal ingredients")

# notFou = dict()

## goes back to see if any word subset from odd ingredients match

# for ing in notFound:
#     if notFound[ing] > 0:
#         # plit = ing.split(" ")
#         found = False
#         # for j in range(len(plit)):
#         #     for i in range(j, len(plit) - j):
#         #         if j == 0:
#         #             stri = " ".join(plit[i:])
#         #         else: 
#         #             stri = " ".join(plit[i:-j])
#         #         if stri in newIngredient:
#         #             newIngredient[ing] = [True, newIngredient[stri][1]]
#         #             found = True
#         #             break
#         #     if found: break
#         #     for i in range(1, len(plit)-j):
#         #         stri = " ".join(plit[j:-i])
#         #         if stri in newIngredient:
#         #             newIngredient[ing] = [True, newIngredient[stri][1]]
#         #             found = True
#         #             break
#         #     if found: break
#         if not found: 
#             if ing in notFou:
#                 print(ing)
#                 notFou[ing] += 1
#             else:
#                 notFou[ing] = 1

# print("looked through odd ingredients")

## attempts to correct the spelling of the last ingredients to find matches

# d = enchant.Dict("en_US")
# corrections = dict()
# for ing in notFou:
#     split = ing.split(" ")
#     stri = ""
#     for word in split:
#         if len(word) > 0 and not d.check(word):
#             suggestions = d.suggest(word)
#             if len(suggestions) > 0:
#                 stri += (suggestions[0] +  " ")
#                 corrections[ing] = suggestions[0]
#         else:
#             stri += (word + " ")
#     corrections[ing] = stri[:-1]

# print("made spelling corrections")

# notfo = dict()

# for ing in corrections:
#     if corrections[ing] in newIngredient:
#         continue
#     else:
#         if ing in notfo:
#             print(ing)
#             notfo[ing] += 1
#         else:
#             notfo[ing] = 1

# print("relooked with corrections")

# newNewIngredient = copy.deepcopy(newIngredient)
# # notFoun = copy.deepcopy(notFound)
# empty = False

## re looks through already added ingredients in newIngredients to see if a subset of any of the consc words are matches

# while not empty:
#     oldIngs = copy.deepcopy(newNewIngredient)
#     newNewIngredient.clear()
#     for ing in oldIngs:
#         plit = ing.split(" ")
#         found = False
#         for j in range(len(plit)):
#             for i in range(j, len(plit) - j):
#                 if j == 0:
#                     stri = " ".join(plit[i:])
#                 else: 
#                     stri = " ".join(plit[i:-j])
#                 if stri in notfo and notfo[stri] > 0:
#                     newNewIngredient[stri] = [True, newIngredient[ing][1]]
#                     found = True
#                     notfo[stri] = 0
#                     break
#             if found: break
#             for i in range(1, len(plit)-j):
#                 stri = " ".join(plit[j:-i])
#                 if stri in notfo and notfo[stri] > 0:
#                     newNewIngredient[stri] = [True, newIngredient[ing][1]]
#                     found = True
#                     notfo[stri] = 0
#                     break
#             if found: break
#         # if not found: 
#         #     if ing in notFoun:
#         #         notFoun[ing] += 1
#         #     else:
#         #         notFoun[ing] = 1
#     newIngredient.update(newNewIngredient)
#     if len(newNewIngredient) == 0:
#         empty = True
#     else: 
#         print("num of new ing: " + str(len(newNewIngredient)))
#         # notFoun.clear()

# print("relooked normal with corrections")

# notF = dict()

## finally looks through to see if any subset of words from odd ingredients matches

# for ing in notfo:
#     if notfo[ing] > 0:
#         plit = ing.split(" ")
#         found = False
#         for j in range(len(plit)):
#             for i in range(j, len(plit) - j):
#                 if j == 0:
#                     str = " ".join(plit[i:])
#                 else: 
#                     str = " ".join(plit[i:-j])
#                 if str in newIngredient:
#                     newIngredient[ing] = [True, newIngredient[str][1]]
#                     found = True
#                     break
#             if found: break
#             for i in range(1, len(plit)-j):
#                 str = " ".join(plit[j:-i])
#                 if str in newIngredient:
#                     newIngredient[ing] = [True, newIngredient[str][1]]
#                     found = True
#                     break
#             if found: break
#         if not found: 
#             if ing in notF:
#                 print(ing)
#                 notF[ing] += 1
#             else:
#                 notF[ing] = 1

# print("looked through odd ingredients")

# make sure to have nil as an ingredient 
keepIngredient = ["nil"]
keepRoot = ["nil"]
# noFound = []

# only add ingredients that are in the recipe dataset
for key in newIngredient:
    if newIngredient[key][0]:
        keepIngredient.append(key)
        keepRoot.append(newIngredient[key][1])

# for key in notFound:
#     if notFound[ing] >=1:
#         noFound.append(key)

print("Ready to make CSV")

df = pd.DataFrame({'ingredient':keepIngredient, 'root':keepRoot}) 
df.to_csv('modified/ingredient-root-was-modified.csv', index=False, encoding='utf-8')

dfL = pd.DataFrame({'ingredient':notFound.keys()}) 
dfL.to_csv('modified/odd-ingredients.csv', index=False, encoding='utf-8')

print("Done")