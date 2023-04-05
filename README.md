# SoupAI
SoupAI uses a stochastic data graph of ingredients in recipes to create a robust soup recipe from user-input ingredeints.


## Project Structure
By default, the project assumes the following directory structure:
 
    +-- dataset                                    # Files that are within GitHub's file size limit
    ¦   +-- recipes-dataset.csv                           # A word embedding model, will be used in utils.tree
    ¦   
    ¦   +-- ingredients                   # Examples of testing data, n=5
    ¦       +-- makeAlias.py                          # Inputs in testing set (directory of .txt files)
    ¦       +-- updateLiquid.py                          # Inputs in testing set (directory of .txt files)
    ¦       +-- webScraping.py                          # Inputs in testing set (directory of .txt files)
    ¦       +-- modified                          # Inputs in testing set (directory of .txt files)
    ¦           +-- ingredient-root-was-modified-wliquid.csv
    ¦       +-- original                          # Human-written outputs in testing set (directory of .txt files)
    ¦           +-- ingredient-root.csv                          # Inputs in testing set (directory of .txt files)
    ¦           +-- liquid-ingredient-root.csv                          # Inputs in testing set (directory of .txt files)  
    ¦   
    +-- ingredientBasedModelCreator.py                                # Files that exceeds GitHub's file size limit
    +-- ingredientBasedSoupMaker.py                           # files created by notebook 3 using data.pickle   
    ¦   
    +-- model                               
    ¦   +-- ing-based-ingredient-model.csv             # Useful for data pre-processing
    ¦   +-- ing-based-soup-ingredient-model.csv                      # Useful for analyzing the generated texts

## Download related files
We share the dataset, model, and related files at [OneDrive](https://1drv.ms/u/s!AnHFRPEgz5RWuwaBg_RdnTTE2d86?e=BU4DQh)
Please download and put them under the correct directory.
```
RecipeGPT-exp/big_data/
RecipeGPT-exp/training/gpt-2/models/
RecipeGPT-exp/recipe1M_1218/

```
