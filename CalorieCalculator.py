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
calorieSum = 0 # total sum of calories
for row in recipeReader:
    ingredient = row[0]

# Perform google search for ingredient

    googleQuery = requests.get('https://www.google.com/search?q=how+many+calories+in+' + ingredient)
    googleQuery.raise_for_status() # test to make sure it's a real web page
    googlePageHTML = bs4.BeautifulSoup(googleQuery.text, 'html.parser')
    
    caloriesFromGoogle = googlePageHTML.select('._Oqb')

# Scrape number of calories from google search

    caloriesInt = caloriesFromGoogle[0].text.split(' ', 1)[0] # strip 'calories' from selected string
    
    
# Write the cell next to next to ingredient and multiply by serving size

    row[2] = caloriesInt
    servingMultiplier = float(row[1].split(' ', 1)[0]) # column 3
    row[3] = int(caloriesInt) * servingMultiplier
    recipeWriter.writerow(row)

# Sum calories of ingredients

    calorieSum += row[3]

# Close files

recipeInFile.close()
recipeOutFile.close()

print(calorieSum)
