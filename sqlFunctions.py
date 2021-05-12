# Cian Hogan GMIT Data Analytics
# Applied Databases Module Project
# SQL based functions file, to be imported to main.py and accessing queries from queries file

# importing packages and other files
import pymysql # for connecting to MySql db
import re # Used for data validation
import queries as q # access SQL queries
import main # imported to return to main menu


"""
sqlFunctions File is used to store procedures for accessing the MySql DB
connect function used to connect to the mySQL DB moviesDB
Many of the functions use sub-routines to collect input from the user and validate it using
built in python functions or regular expressions
SQL syntax queries are imported from the queries file to reduce clutter
"""


# setting the SQL connection variable
conn = None

# Connect to SQL DB 
def connect():
	global conn

	conn = pymysql.connect(host="localhost", user='root', password='', 
		db="moviesDB", cursorclass=pymysql.cursors.DictCursor)


# Function for Menu choice 1
def viewFilms():
	global conn

	# connect to SQL DB
	if not conn:
		connect()

	print("""
Films
-----"""
	)

	count = 0

	with conn:
		with conn.cursor() as cursor: # initialize sql connection cursor object

			cursor.execute(q.viewFilm) # use cursor to execute query
			res = cursor.fetchall() # store query results in var res

			# Only shows 5 results at a time
			# If user gets to the end of the results will be told and returned to main menu
			while count < len(res):

				for i in res[count:count+5]:
					film, actor = i["FilmName"], i["ActorName"]
					print(film +'  :   '+ actor)

				userIn = input("--Quit (q)--")

				# returns to main menu if user inputs q or quit
				if userIn.lower() == "quit" or userIn.lower() == "q":
					conn = None
					main.main()

				else:
					count += 5 # increment to show next 5 results


			print("All Records Shown: Returning to Main Menu")
			conn = None # reset conn to none to avoid error/exception
			main.main()



# Sub-Function for Menu choice 2
def getYear():
	# regex used to make sure user eneters a valid year
	year = input("Year of Birth : ")
	regex = re.compile("19|20\d\d")

	if regex.match(year):
		return year
	else:
		print("Minimum year 1900: Year must match format yyyy")
		return getYear() # recursion if user input is incorrect


# Second Sub-Function for Menu choice 2
def getGender():
	gender = input("Gender (Male/Female) : ")

	if gender == "": # return none if no gender entered
		return None

	elif gender.lower() == "f" or gender.lower() == "female":
		return "Female"

	elif gender.lower() == "m" or gender.lower() == "male":
		return "Male"

	else:
		return getGender() # recursion if user input is incorrect

# Main Function for Menu choice 2		
def actorByYear():
	global conn

	print("""
Actors
------""")

	# Uses subfunctions to get input
	year = getYear()
	gender = getGender()

	# uodates query with user input
	query = q.actorByYearWithGender % (year, gender)

	# if no gender is input by user use a different query
	if gender == None:
		query = q.actorByYear % (year)

	if not conn:
		connect() # connect to SQL DB

	with conn:
		with conn.cursor() as cursor: # intialise cursor object

			cursor.execute(query)
			res = cursor.fetchall() # store query results in res

			if len(res) == 0:
				print("No Matches found:")
				actorByYear()

			else:

				print("""
Actor   :   Month   :   Gender
-------------------------------""")

				for i in res:
					actor, month, actorGender = i["ActorName"], i["Month"], i["ActorGender"]
					print(actor +'  :   '+ month+'   :   '+actorGender)

	conn = None # reset conn to none

	main.main() # return to main menu


def viewStudios():
	global conn

	if not conn:
		connect() # connect to DB

	with conn:
		with conn.cursor() as cursor:

			cursor.execute(q.viewStudios) # query from queries file
			res = cursor.fetchall()

	conn = None

	return res # returns query result to var in main file


# sub functions for menu option 4
def getCountryID():
	newID = input("ID : ")
	# if input can't be converted to int start again
	try:
		newID = int(newID)
		if newID <= 0: # make sure its a positive int >0
			print("ID must be greater than 0")
			return getCountryID()
		else:
			return newID
	except:
		print("Enter a valid ID")
		return getCountryID() # recursion if user input is incorrect

# sub functions for menu option 4
def getCountryName():
	# regex to not allow numbers or special chars
	regex = re.compile("[a-zA-Z][a-zA-Z]+")
	newCountryName = input("NAME : ")

	if len(newCountryName) == 0 or not regex.match(newCountryName):
		print("Enter a valid name")
		return getCountryName() # recursion if user input is incorrect

	else:
		# convert to capital and return value
		newCountryName = newCountryName.capitalize()
		return newCountryName
	
# Option 4 add new country
def addCountry():
	# User sub func's for input
	newCountryID = getCountryID()
	newCountryName = getCountryName()

	global conn
	
	if not conn:
		connect() # connect to sql DB

	with conn:
		with conn.cursor() as cursor:
			# Update query from queries file
			query = q.addNewCountry % (newCountryID, newCountryName)

			try:
				cursor.execute(query)

				conn.commit() # commit changes to DB
				# Print success message to user
				print("Country: %s, %s added to database" % (newCountryID, newCountryName))

			except: # If country already exists an error is raised
				print("***Error***: ID and/or Name ( %s , %s) already exists " % (newCountryID, newCountryName))
	
	# whether a country is added or not returns to main menu
	conn = None # reset conn
	main.main()		

# Option 5 SQL component
def viewSubtitleMovies(query):
	global conn

	if not conn:
		connect() # connect to DB

	with conn:
		with conn.cursor() as cursor:

			# Executes query parameter and displays results
			cursor.execute(query)
			res = cursor.fetchall()

			for i in res:
					
				print(str(i["Name"]) +'  :   ' + i["Synopsis"])

	conn = None

	main.main()


# Option 6 SQL component
def checkMovieExists(movieID):
    global conn

    if not conn:
        connect()
    # Movie ID from main is checked in SQL DB to make sure it exists
    query = q.movieExists % (movieID)

    with conn:
        with conn.cursor() as cursor:

            cursor.execute(query)
            res = cursor.fetchall()

    conn = None
    # If the query returns an empty result it returns false 
    # meaning it does not exist in SQL DB
    if len(res) == 0:
    	return False
    else: 
    	return True

