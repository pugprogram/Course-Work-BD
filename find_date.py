from datetime import datetime 
from calendar import monthrange
import sqlite3

text="Сегодняшняя дата: " + str(datetime.now().day) +".0"+ str(datetime.now().month) + "." +str(datetime.now().year)+ '''\nПоказать запланированные дела? '''

def func_for_date(username,faculty,array_chislitel,array_znamenatel):	
	current_year=datetime.now().year
	month=2
	firstr=0
	chetn=1
	chislo=6
	firstdate="06.02.2023"
	num_of_week=1
	scetchik=0
	weekday=0
	Week=['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
	variableForSubject=0
	
#Недель всего 17
#Воскресенья нет


	


	while True:
		if (firstr!=0):
			scetchik+=1
		
			if (num_of_week==18):
				break
			if (weekday==6):
				weekday=0
			if (scetchik==6):
				if (chislo+1)>monthrange(current_year,month)[1]:
					chislo=2
					month+=1
				elif (chislo+1)==monthrange(current_year,month)[1]:
					chislo=1
					month+=1
				else:
					chislo+=2
				num_of_week+=1
				if chetn==1:
					chetn=0
					variableForSubject=0
				else:
					chetn=1
					variableForSubject=0
			elif (scetchik!=6) and (chislo+1)<=monthrange(current_year,month)[1]:
				chislo+=1
			else:
				chislo=1
				month+=1
			if scetchik==6:
				scetchik=0
			if (chislo<10):
				firstdate='0'
		firstr=1	
		firstdate=str(chislo)+'.'+"0"+str(month)+'.'+str(current_year)	

		#INSERT INTO SUBJECT

		for i in range (0,7):

			if (chetn==0):
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()					
				sqlite_query='''INSERT INTO SUBJECT (DATE1,DAY_WEEK,SUBJECT_name,TIME1,FACULTY,USERNAME) 
				SELECT \''''+ firstdate+'\',\''+array_chislitel[variableForSubject][0]+'''\',\''''+array_chislitel[variableForSubject][2]+'''\',\''''+array_chislitel[variableForSubject][1]+'''\'
				, \''''+faculty+'''\',\''''+username+'''\' WHERE NOT EXISTS (SELECT* FROM SUBJECT WHERE USERNAME =
				\''''+username+'\' AND FACULTY= \''+faculty+'\' AND TIME1= \''+array_chislitel[variableForSubject][1]+ '\' AND DATE1= \''+firstdate+'\');'
				cursor.execute(sqlite_query)
				sqlite_connection.commit()
				cursor.close()
				variableForSubject+=1
			else:
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				sqlite_query='''INSERT INTO SUBJECT (DATE1,DAY_WEEK,SUBJECT_name,TIME1,FACULTY,USERNAME) 
				SELECT \''''+ firstdate+'\',\''+array_znamenatel[variableForSubject][0]+'''\',\''''+array_znamenatel[variableForSubject][2]+'''\',\''''+array_znamenatel[variableForSubject][1]+'''\', \''''+faculty+'''\',\''''+username+'''\' WHERE NOT EXISTS (SELECT* FROM SUBJECT WHERE USERNAME =
				\''''+username+'\' AND FACULTY= \''+faculty+'\' AND TIME1= \''+array_znamenatel[variableForSubject][1]+ '\' AND DATE1 = \''+firstdate+'\');'
				cursor.execute(sqlite_query)
				sqlite_connection.commit()
				cursor.close()
				variableForSubject+=1




		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		sqlite_query='''INSERT INTO WEEK (CHET,NUMOFWEEK,USERNAME,FACULTY) 
		SELECT \''''+ str(chetn)+'\',\''+str(num_of_week)+'''\',\'
		'''+username+'''\',\''''+faculty+'''\' WHERE NOT EXISTS (SELECT* FROM WEEK WHERE USERNAME =
		\''''+username+'\' AND FACULTY= \''+faculty+'\');'
		cursor.execute(sqlite_query)
		sqlite_connection.commit()
		cursor.close()
		
		
		#CREATE TABLE IF NOT EXISTS DAYWEEK(
		#ID INTEGER PRIMARY KEY AUTOINCREMENT,
		#DATE TEXT UNIQUE NOT NULL,
		#NUMOFWEEK INTEGER,
		#USERNAME TEXT,
		#FACULTY TEXT,
		#FOREIGN KEY (USERNAME) REFERENCES USERS_INFO (TELEGRAMID),
		#FOREIGN KEY (NUMOFWEEK) REFERENCES WEEK (NUMOFWEEK)
		#);

		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		sqlite_query='''INSERT INTO DAYWEEK (DATE,NUMOFWEEK,USERNAME,FACULTY,DAYOFWEEK) 
		SELECT \''''+ firstdate+'\',\''+str(num_of_week)+'''\',\'
		'''+username+'''\',\''''+faculty+'''\',\''''+Week[weekday]+'''\' WHERE NOT EXISTS (SELECT* FROM DAYWEEK WHERE DATE =
		\''''+firstdate+'\');'
		cursor.execute(sqlite_query)
		sqlite_connection.commit()
		cursor.close()		
		
		#CREATE TABLE IF NOT EXISTS SUBJECT (
		#ID INTEGER PRIMARY KEY AUTOINCREMENT,
		#DATE TEXT UNIQUE NOT NULL,
		#SUBJECT_name TEXT NOT NULL, 
		#TIME TEXT,
		#FACULTY TEXT,
		#USERNAME TEXT,
		#FOREIGN KEY (USERNAME) REFERENCES USERS_INFO (TELEGRAMID),
		#FOREIGN KEY (DATE) REFERENCES DAYWEEK (DATE)
		#);
		
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		weekday+=1
		
		
		
		
		
