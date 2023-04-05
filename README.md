# SoupAI
SoupAI uses a stochastic data graph of ingredients in recipes to create a robust soup recipe from user-input ingredeints.


## Project Structure
By default, the project assumes the following directory structure:
 
    +-- dataset                                           # Dataset information
    ¦   +-- recipes-dataset.csv                           # renamed recipe database, must be downloaded, exceedes max file size
    ¦   
    ¦   +-- ingredients                                   # Ingredients information
    ¦       +-- makeAlias.py                              # creates ingredient dict
    ¦       +-- updateLiquid.py                           # creates ingredient dict
    ¦       +-- webScraping.py                            # creates ingredient dict
    ¦       +-- modified                                  # Modified ingredient dict
    ¦           +-- ingredient-root-was-modified-wliquid.csv   # Ingredient dict used in model
    ¦       +-- original                                  # Original ingredients data from webscraping
    ¦           +-- ingredient-root.csv                   # Original ingredients mapped to their root ingredient
    ¦           +-- liquid-ingredient-root.csv            # Original liquid ingredients mapped to their root ingredient 
    ¦   
    +-- ingredientBasedModelCreator.py                    # Creates ingredient model to create soups
    +-- ingredientBasedSoupMaker.py                       # Main soup maker that generates ingredient lists
    ¦   
    +-- model                                             # Stores ingredient models used in the soup maker                            
    ¦   +-- ing-based-ingredient-model.csv                # Ingredient model for all recipes 
    ¦   +-- ing-based-soup-ingredient-model.csv           # Ingredient model for soup recipes

ing-based-ingredient-model.csv and ing-based-soup-ingredient-model.csv are generated when ingredientBasedModelCreator.py is ran
python3 ingredientBasedModelCreator.py
The database RecipeNGL should be downloaded, renamed to recipes-dataset.csv, and placed in the dataset directory
run python3 ingredientBasedSoupMaker.py to generate soup ingredients

## Download related files
Please download, rename and put them under the correct directory. 

RecipeNGL: https://recipenlg.cs.put.poznan.pl/
