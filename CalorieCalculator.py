# This project is intended to calculate the calories for a list of ingredients in a CSV spreadsheet

import bs4, csv, os, requests

# Open recipe file

# print('What is the name of the recipe?')
# recipeName = input()

# recipeInFile = open('c:\\users\\ndpayne\\MyPythonScripts\\' + recipeName + '.csv')

os.chdir('c:\\users\\ndpayne\\calorieScraper')
recipeInFile = open('Dense_Salad_With_Lemon_Honey_Dressing.csv')
recipeOutFile = open('Dense_Salad_With_Lemon_Honey_Dressing_Output.csv', 'w', newline='')
recipeReader = csv.reader(recipeInFile)
recipeWriter = csv.writer(recipeOutFile)

# Read ingredient from appropriate cell

next(recipeReader) # skip the header row
for row in recipeReader:
    ingredient = row[0]

# Perform google search for ingredient

    googleQuery = requests.get('https://www.google.com/search?q=how+many+calories+in+' + ingredient)
    googleQuery.raise_for_status() # test to make sure it's a real web page
    googlePageHTML = bs4.BeautifulSoup(googleQuery.text, 'html.parser')
    
    caloriesFromGoogle = googlePageHTML.select('._Oqb')

# Scrape number of calories from google search

    caloriesInt = str(caloriesFromGoogle[0].text.split(' ', 1)[0]) # strip 'calories' from selected string
    
    
# Write the cell next to next to ingredient

    row[2] = caloriesInt
    recipeWriter.writerow(row)

# Close files

recipeInFile.close()
recipeOutFile.close()

# TODO - Multiply calorie amount by serving size

# TODO - Sum calories of ingredients
