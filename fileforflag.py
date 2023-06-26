import sqlite3
dictforflag={}
dictfordata={}
dictfortime={}
dictforfaculty={}

flag=0
data=""
def FindFaculty(message):
	sqlite_connection = sqlite3.connect('sqlite_python.db')
	cursor = sqlite_connection.cursor()
	sqlite_query='''SELECT FACULTY_NAME FROM FACULTY
	WHERE USERNAME=\''''+ message +"\';"
	cursor.execute(sqlite_query)
	findmas=cursor.fetchall()
	cursor.close()
	return findmas
