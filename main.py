# Cian Hogan GMIT Data Analytics
# Applied Databases Module Project
# Main application file to be run

# importing packages and files
import sqlFunctions as sql # SQL based code
import mongoFunctions as mongo # Mongo based code
import queries as q # File with SQL queries
import pymongo # imported for exceptions

"""
Main Menu has 6 choices and an option to close the programme (x).
The choices call functions from the appropriate DB function files (mySql & MongoDB).
Some SQL queries are used from within the main file.
Some variables are stored in the main file either to store data so we don't ahve to access the DB again
or to transfer results from one DB type to the other.
"""


def main():
	startMenu()
	# Get user input
	choice = input("Choice: ")
	# User inputs x to close application
	if choice.lower() == "x":
		print("Closing Programme")
		quit()

	elif choice == "1":
		sql.viewFilms()

	elif choice == "2":
		sql.actorByYear()

	elif choice == "3":
		#Access global studios variable which will store results
		global studios 

		# If the variable has already stored result not load from DB again
		if studios == None:
			studios = sql.viewStudios() 

		print("""
Studios
-------""")
		# Printing studio ID and name	
		for studio in studios:
					
			print(str(studio["StudioID"]) +'  |   ' + studio["StudioName"])

		main() # Return to main menu

	elif choice == "4":
		sql.addCountry()

	elif choice == "5":
		# Store mongo results in var
		langMovies = mongo.findSubtitles()

		# Tell user if no results, return to menu
		if len(langMovies) == 0:
			print("No movies found")
			main()

		else:
			# format results for SQL query
			langMovies = str(langMovies).strip("[]")

			query = q.moviesWithSubtitles % langMovies

			sql.viewSubtitleMovies(query)
		

	elif choice == "6":
		# Store results in Var
		movieScript = mongo.getNewScript()

		# Check if the movie exists in SQL DB
		if sql.checkMovieExists(movieScript["_id"]):
			
			try:
				mongo.addScript(movieScript)
				print("MovieScript: %s added to database" % (movieScript["_id"]))
				main()
			# Only return error if script already exists in Mongo DB
			except pymongo.errors.DuplicateKeyError: 
				print("""
*** ERROR ***: Movie Script with id: %s already exists""" % (movieScript["_id"]))
				main()

		else: # If the movie doesn't exist in SQL DB
			print("""
*** ERROR ***: Film with id: %s does not exist in moviesDB""" % (movieScript["_id"]))
			main()

	else: # any incorrect input returns to start
		main()


# Start Menu Function displays choices
def startMenu():
	print("""
MENU
====
1 - View Films
2 - View Actors by Year of Birth & Gender
3 - View Studios
4 - Add New Country
5 - View Movie with Subtitles
6 - Add New Movie Script
x - Exit application""")	

# Set global variable studios to be used in main function
studios = None


# Executes the main function if the file is the main program being run
if __name__ == "__main__":
	main()