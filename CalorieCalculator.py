import bs4, csv, os, requests

############################
# initial option path tree #
############################
def initUserInput():
    while True:
        userChoice = input()
        if userChoice == '1':
            userChoiceOne()
        elif userChoice == '2':
            userChoiceTwo()
        elif userChoice == '3':
            print('You entered 3.')
        else:
            invalidEntry()
            continue
        
        # checks whether user wants to re-enter path 1/2/3 after branch completion
        moreAction()
        break

############################        
#### Option 1 functions ####
############################
def userChoiceOne():
    # pretty print recipe file names
    print('Here is the list of recipes you\'ve created.')
    recipeList = listRecipes()
    for recipe in recipeList:
        print(recipe)

    print('Type in the name of the recipe you would like to view.')
    # prints individual recipe file info that user selects 
    while True:
        recipeNameInput = input()
        if recipeNameInput not in recipeList:
            invalidEntry()

        # prints out info from selected recipe file    
        else:
            with open(recipeNameInput + '.csv', newline='') as recipeFile:
                recipeReader = csv.reader(recipeFile)
                calorieSum = 0
                for row in recipeReader:
                    # row[0] = ingredient name, row[1] = amount, row[3] = calories for ingredient
                    print('{} - {} - {} calories'.format(row[0], row[1], row[3]))
                    calorieSum += float(row[3])
            print('Total calories: ' + str(calorieSum))
            break

# returns list of recipes located in repository
def listRecipes():
    for folderName, subfolders, filenames in os.walk('.'):
        prettyFiles = [filename.split('.csv')[0] for filename in filenames]
    return prettyFiles
        
############################        
#### Option 2 functions ####
############################
def userChoiceTwo():
    recipeList = listRecipes()
    recipeName = input('What is the name of your recipe?\n')
    if recipeName not in recipeList:
        print('Type the ingredient followed by the amount.\n' \
              'e.g. Broccoli - 2 heads.\n' \
              'If you are finished listing ingredients, type \'done\'.')
        # create new file and write ingredients to it
        with open(recipeName + '.csv', 'w', newline='') as recipeFile:
            recipeWriter = csv.writer(recipeFile)
            while True:
                ingredient = input()
                if ingredient == 'done':
                    break
                else:
                    # turn input into list
                    ingredientRow = [x.strip() for x in ingredient.split('-')]
                    # if list has length two and the second element is an int or float continue
                    if len(ingredientRow) == 2 and isNumber(ingredientRow[1]):
                        recipeWriter.writerow(ingredientRow)
                    else:
                        invalidEntry()
    else:
        print('That recipe already exists.')
        userChoiceTwo()

# test to make sure that amount starts with a number
def isNumber(amount):
    testNumber = amount.split()[0]
    try:
        float(testNumber)
        return True
    except ValueError:
        return False

##########################

# tests whether user wants to start at top of tree again
def moreAction():
    while True:
        userInput = input('Is there anything else you\'d like to do today? (yes/no)\n')
        if not moreActionInput(userInput):
            break
def moreActionInput(userInput):
        if userInput == 'no':
            return False
        elif userInput == 'yes':
            print(optionPaths)
            initUserInput()
        else:
            invalidEntry()
            return True

def invalidEntry():
    print('Invalid entry, please try again.')

##########################


optionPaths = 'Enter 1 to view the list of existing recipes.\n'\
              'Enter 2 to add a new recipe.\n'\
              'Enter 3 to search for a recipe by ingredient.'
os.chdir('c:\\users\\ndpayne\\calorieScraper\\recipe_repo')
print('Hello! Welcome to your recipe program.\n\n' + optionPaths)

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
