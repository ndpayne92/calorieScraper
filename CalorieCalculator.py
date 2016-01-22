import bs4, csv, os, requests

def introduction():
    os.chdir('c:\\users\\ndpayne\\calorieScraper')

    print('Hello! Welcome to your recipe program.\n\n' \
          'Enter 1 to view the list of existing recipes.\n' \
          'Enter 2 to add a new recipe.\n'
          'Enter 3 to search for a recipe by ingredient.')

def initUserInput():
    
    invalidEntry = True
    while invalidEntry:
        userChoice = input()
        
        if userChoice == '1':
            userChoiceOne()
            invalidEntry = False
            
        elif userChoice == '2':
            print('You entered 2.')
            invalidEntry = False
            
        elif userChoice == '3':
            print('You entered 3.')
            invalidEntry = False
            
        else:
            print('You didn\'t enter a valid character, please try again.')

    moreInput = True
    while moreInput:
        userInput = input('Is there anything else you\'d like to do today? (yes/no)\n')
        moreInput = moreAction(userInput)
    
# If user inputs option one
def userChoiceOne():
            print('Here is the list of recipes you\'ve created.')
            recipeList = listRecipes()
            for recipe in recipeList:   # pretty print recipe file names
                print(recipe)
            
            print('Type in the exact name of the file you would like to view including filetype.')
            viewSpecRecipe(recipeList)  # prints individual recipe file info
            

# returns list of filenames (e.g. recipes) in the recipe repository
def listRecipes():
    for folderName, subfolders, filenames in os.walk('recipe_repo'):
        return filenames

# prints relevant info from recipe file
def viewSpecRecipe(recipeList):
    
    while True:
        recipeNameInput = input().strip()
        
        if (recipeNameInput) not in recipeList:     # checks user input recipe for existance in recipe_repo
            print('What you entered isn\'t a valid recipe. Please enter a recipe name again.')

        # prints out info from selected recipe file    
        else:
            recipeFile = open('recipe_repo\\' + recipeNameInput)
            recipeReader = csv.reader(recipeFile)

            calorieSum = 0
            for row in recipeReader:
                print(row[0] + ' - ' + row[1] + ' - ' + row[3] + ' calories') # row[0] = ingredient name, row[1] = amount, row[3] = calories for ingredient
                calorieSum += float(row[3]) # row[3] = total calories for a single ingredient
            print('Total calories: ' + str(calorieSum))
            recipeFile.close()
            break


def moreAction(userInput):
        if userInput == 'no':
            return False
        
        elif userInput == 'yes':
            print('Enter 1 to view the list of existing recipes.\n' \
                  'Enter 2 to add a new recipe.\n'
                  'Enter 3 to search for a recipe by ingredient.')
            initUserInput()
        else:
            print('You didn\'t input a valid entry.')
            return True

introduction()
initUserInput()

print('Exiting program.')

'''



# Open recipe file

recipeInFile = open('Dense_Salad_With_Lemon_Honey_Dressing.csv')
recipeOutFile = open('recipe_repo\\Dense_Salad_With_Lemon_Honey_Dressing.csv', 'w', newline='')
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

    caloriesInt = caloriesFromGoogle[0].text.split(' ', 1)[0] # 65 calories --> 65
    
    
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

'''
