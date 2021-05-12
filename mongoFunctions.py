# Cian Hogan GMIT Data Analytics
# Applied Databases Module Project
# MongoDB based functions file, to be imported to main.py

# Import packages and other files needed
import pymongo # # for connecting to Mongo db
import re # Used for data validation
import main # imported to return to main menu


"""
mongoFunctions File is used to store procedures for accessing the Mongo DB
Many of the functions use sub-routines to collect input from the user and validate it using
built in python functions or regular expressions
"""


# Sub function for option 5 used to get user input
def getLang():
	# Uses regex to try to validate the user input
	regex = re.compile("[a-zA-Z][a-zA-Z]+")
	subtitleLang = input("Enter subtitle Language : ")
	# Capitalize user input
	subtitleLang = subtitleLang.capitalize()
	
	if len(subtitleLang) == 0 or not regex.match(subtitleLang):
		print("Enter a valid Language name")
		return getLang() # Recursion if incorrect input

	else:
		return subtitleLang

# Option 5 in main menu
def findSubtitles():

	print("""

Movies with Subtitles
----------------------""")
	# Calls sub function to set var for language
	lang = getLang()
	# creates empty list var for results
	movieList = []
	# Connect to pymongo client
	client = pymongo.MongoClient()
	# connect to DB
	mydb = client["movieScriptsDB"]
	# access the MovieScripts collection
	coll = mydb["movieScripts"]
	# find records with subtitles that match the input language
	results = coll.find({'subtitles':lang})

	# add ID's from results to movie list
	for i in results:
		movieList.append(i["_id"])

	printHeader = """
Movies with %s subtitles""" % lang
		
	print(printHeader)
	print("-"*(len(printHeader)-1))

	client.close() # close mongo client

	return movieList #return the list of movie IDs

# Option 6 user input sub functions
def getID():
	newID = input("ID : ")

	try:
		newID = int(newID)
		if newID <= 0: # make sure id is positive number
			print("ID must be greater than 0")
			return getID()

		else:
			return newID
	
	except:
		print("ID must be a number")
		return getID() # Recursion if val cant be converted to int

# Option 6 user input sub functions
def getKeyword():
	kWord = input("Keyword (-1 to end): ")
	if len(kWord) == 0: # if user enters blank return
		return getKeyword()

	else:
		return kWord

# Option 6 user input sub functions
def getSubLang():
	
	subtitleLang = input("Subtitles Language (-1 to end): ")

	subtitleLang = subtitleLang.capitalize()
	
	if len(subtitleLang) == 0: # if user enters blank return
		return getSubLang()

	else:
		return subtitleLang

# Option 6 function used to get users input of a movie script
def getNewScript():

	newID = getID() # Get user input  ID

	kWordList, subLangList = [], [] # initialize 2 empty lists

	kWord = None # set none value

	# loop exits when user enters -1
	while kWord != "-1":

		if kWord != None: # on the first run nothing happens
			kWordList.append(kWord)

		kWord = getKeyword() # gets user input

	# same loop as before with language instead of keyword
	subLang = None

	while subLang != "-1":

		if subLang != None:
			subLangList.append(subLang)

		subLang = getSubLang()

	# create a mongdodb doc structure
	doc = {"_id":newID, "keywords":kWordList, "subtitles":subLangList}

	return doc

# Option 6 adds new script to the Mongo DB
def addScript(movieScript):
	# connect to mongo DB
	client = pymongo.MongoClient()

	mydb = client["movieScriptsDB"]

	coll = mydb["movieScripts"]

	# insert new script document
	coll.insert_one(movieScript)

	client.close() # close mongo client

