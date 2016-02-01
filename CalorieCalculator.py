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
                    print('{} - {} - {} calories'.format(row[0], row[1], row[2]))
                    calorieSum += float(row[2])
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
                    ingredientList = [x.strip() for x in ingredient.split('-')]
                    # if list has length two and the second element is an int or float continue
                    if len(ingredientList) == 2 and isNumber(ingredientList[1]):
                        print('Calculating calorie value...')
                        # query google for ingredient
                        googleQuery = requests.get('https://www.google.com/search?q=how+many+calories+in+' + ingredientList[0])
                        # test to see if real web page
                        googleQuery.raise_for_status()
                        # grab selector
                        googlePageHTML = bs4.BeautifulSoup(googleQuery.text, 'html.parser')
                        caloriesFromGoogle = googlePageHTML.select('._Oqb')
                        # convert to just a number
                        try:
                            caloriesInt = caloriesFromGoogle[0].text.split(' ', 1)[0]
                        except:
                            print('Cannot find ingredient, please enter another.')
                            continue
                        servingMultiplier = float(ingredientList[1].split(' ', 1)[0])
                        ingredientList.append(int(caloriesInt) * servingMultiplier)                    
                        recipeWriter.writerow(ingredientList)
                        print('Enter next ingredient.')
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
