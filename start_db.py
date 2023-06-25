import sqlite3

def CloseDB(sqlite_connection):
	if (sqlite_connection):
			sqlite_connection.close()
			print("Соединение с SQLite закрыто")
def ConnectDB():	
	try:
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		print("База данных подключена к SQLite")
	
		with open('data_bases.sql', 'r') as sqlite_file:
			sql_script = sqlite_file.read()
    
		cursor.executescript(sql_script)
		print("Скрипт SQLite успешно выполнен")
		cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite", error)
	        
		       
