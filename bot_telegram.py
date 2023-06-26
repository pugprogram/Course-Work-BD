import telebot 
from telebot import types
import Faculty
import download_schedule
import start_db
import sqlite3
import find_date
import re 
import fileforflag
import dictforrightout
from datetime import datetime 
from calendar import monthrange


first=0
token="6277348156:AAFeIDChcSwJNrVBxVfeiCbQdpm1vfs6H3Y"
bot = telebot.TeleBot (token)


@bot.message_handler(commands=['start'])
def start(message):
	fileforflag.dictforfaculty[str(message.from_user.id)]=""
	fileforflag.dictfortime[str(message.from_user.id)]=""
	fileforflag.dictfordata[str(message.from_user.id)]=""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	start_db.ConnectDB()
	sqlite_connection = sqlite3.connect('sqlite_python.db')
	cursor = sqlite_connection.cursor()
	print("База данных подключена к SQLite")
	fileforflag.dictforflag[str(message.from_user.id)]=0
	sqlite_query='''INSERT INTO USER_INFO (TELEGRAMID) 
	SELECT '''+str(message.from_user.id)+'''
	WHERE NOT EXISTS (SELECT* FROM USER_INFO WHERE TELEGRAMID =
	'''+str(message.from_user.id)+');'
	cursor.execute(sqlite_query)
	sqlite_connection.commit()
	print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
	cursor.close()
	btn1 = types.KeyboardButton("Let's go 🧐")
	markup.add(btn1)
	bot.send_message(message.from_user.id, "👋 Привет! Я - бот-помощник, в котором ты можешь хранить своё расписание! Жми кнопку, и мы начнем) ", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def handler_message(message):
	if ((message.text=="Let's go 🧐") or (message.text=="вернуться в главное меню🔙")) and (fileforflag.dictforflag[str(message.from_user.id)]==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("Расписание МГТУ🗓")
		#btn2=types.KeyboardButton("Свое расписание🔮")
		#markup.add(btn1,btn2)
		markup.add(btn1)
		fileforflag.dictfordata[str(message.from_user.id)]=""
		bot.send_message(message.from_user.id," Что бы вы хотели сделать? ",reply_markup=markup)
	elif (message.text=="вернуться в главное меню🔙") and (fileforflag.dictforflag[str(message.from_user.id)]==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictforflag[str(message.from_user.id)]=0
		fileforflag.dictfordata[str(message.from_user.id)]=0
	elif (message.text=="Расписание МГТУ🗓") and (fileforflag.dictforflag[str(message.from_user.id)]==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn=[]
		listofFaculty=Faculty.FindFaculty()
		for i in listofFaculty:
			btn.append(types.KeyboardButton(i))
		btn.append (types.KeyboardButton("вернуться в главное меню🔙"))
		for i in btn: 
			markup.add(i)
		bot.send_message(message.from_user.id,"Выберите свой факультет",reply_markup=markup)
	elif (message.text in Faculty.FindFaculty()) and (fileforflag.dictforflag[str(message.from_user.id)]==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Faculty.faculty=message.text
		btn=[]
		ListOf=Faculty.ListOfNumFaculty(message.text)
		Faculty.ListOfFaculty=ListOf
		for i in ListOf:
			btn.append(types.KeyboardButton(i))
		btn.append (types.KeyboardButton("вернуться в главное меню🔙"))
		for i in btn: 
			markup.add(i)
		bot.send_message(message.from_user.id,"Выберите номер факультета",reply_markup=markup)
	elif (message.text in Faculty.ListOfNumFaculty(message.text)) and (fileforflag.flag==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		fileforflag.dictfordata[str(message.from_user.id)]=""
		btn=[]
		ListOf=Faculty.PrintCourse(message.text)
		Faculty.ListOfCourse=ListOf
		for i in ListOf:
			btn.append(types.KeyboardButton(i))
		btn.append (types.KeyboardButton("вернуться в главное меню🔙"))
		for i in btn: 
			markup.add(i)
		bot.send_message(message.from_user.id,"Выберите свою группу",reply_markup=markup)
	elif (fileforflag.dictforflag[str(message.from_user.id)]==1) and (fileforflag.FindFaculty(str(message.from_user.id))!=None):
		fileforflag.dictfortime[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		fileforflag.dictforflag[str(message.from_user.id)]=0
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		#print(fileforflag.data)
		fileforflag.dictforfaculty[str(message.from_user.id)]=str(message.text)
		sqlite_query='''SELECT DAY_WEEK,TIME1,SUBJECT_NAME FROM SUBJECT
		WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+str(message.text)+'''\'
		AND DATE1= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\';"
		cursor.execute(sqlite_query)
		findmas=cursor.fetchall()
		cursor.close()
		answer_text=""
		#fileforflag.dictfordata[str(message.from_user.id)]=""
		if len(findmas)!=0:
			answer_text=answer_text+dictforrightout.dictionary[findmas[0][0]]+"\n"
			for i in findmas:
				answer_text+=i[1]
				answer_text+='\n'
				answer_text+=i[2]
				answer_text+='\n'
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
				sqlite_query='''SELECT TASK_NAME FROM TASK
				WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
				AND DATE= \''''+str(find)+"\' AND TIME = \'"+i[1]+"\';"
				cursor.execute(sqlite_query)
				findtask=cursor.fetchall()
				cursor.close()
				if (len(findtask)!=0):
					answer_text+=findtask[0][0]
					answer_text+='\n'
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
			sqlite_query='''SELECT TASK_NAME FROM TASK
			WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
			AND DATE= \''''+str(find)+"\' AND TIME = \'\';"
			cursor.execute(sqlite_query)
			findtask=cursor.fetchall()
			cursor.close()
			if (len(findtask)!=0):
				answer_text+=findtask[0][0]
				answer_text+='\n'
			markup.add(types.KeyboardButton("записать свои дела"))
			markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
			bot.send_message(message.from_user.id,answer_text,reply_markup=markup)
		else:
			markup.add(types.KeyboardButton("выбрать другую дату"))
			markup.add(types.KeyboardButton("записать свои дела"))
			markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
			answer_text="занятий в этот день нет)\nможете выбрать другую дату или записать свои собственные дела"
			bot.send_message(message.from_user.id,answer_text,reply_markup=markup)

	elif (message.text in Faculty.PrintCourse(message.text)) and (fileforflag.flag==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Faculty.faculty=message.text
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		print("База данных подключена к SQLite")
		sqlite_query='''INSERT INTO FACULTY (FACULTY_NAME,USERNAME) 
		SELECT \''''+ Faculty.faculty+'\',\''+str(message.from_user.id)+'''\'
		WHERE NOT EXISTS (SELECT* FROM FACULTY WHERE USERNAME =
		\''''+str(message.from_user.id)+'\' AND FACULTY_NAME= \''+Faculty.faculty+'\');'
		cursor.execute(sqlite_query)
		sqlite_connection.commit()
		print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
		cursor.close()
		href=Faculty.FINDALL(Faculty.faculty)
		array_chislitel,array_znamenatel=download_schedule.FindShedule(href)
		#print(array_chislitel)
		#print(array_znamenatel)
		find_date.func_for_date(str(message.from_user.id),Faculty.faculty,array_chislitel,array_znamenatel)
		
		markup.add(types.KeyboardButton("да"))
		markup.add(types.KeyboardButton("выбрать свою дату"))
		markup.add (types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id,find_date.text,reply_markup=markup)
	elif ((message.text=="выбрать другую дату") or (message.text=="выбрать свою дату")) and (fileforflag.flag==0):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		text = "Введите день, месяц, год через пробел в формате 9.05.2022"
		markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id, text,reply_markup=markup)
	elif (re.fullmatch("\d?\d\.0\d\.\d{4}",message.text) and (fileforflag.flag==0)):
		fileforflag.dictforfaculty[str(message.from_user.id)]=""
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=message.text
		find=message.text
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		sqlite_query='''SELECT FACULTY_NAME FROM FACULTY
		WHERE USERNAME=\''''+ str(message.from_user.id)+"\';"
		cursor.execute(sqlite_query)
		findmas=cursor.fetchall()
		cursor.close()
		if (len(findmas)==1):
			print(findmas[0][0])
			fileforflag.dictforfaculty[str(message.from_user.id)]=findmas[0][0]
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			fileforflag.dictforflag[str(message.from_user.id)]=0
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''SELECT DAY_WEEK,TIME1,SUBJECT_NAME FROM SUBJECT
			WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+findmas[0][0]+'''\'
			AND DATE1= \''''+str(find)+"\';"
			cursor.execute(sqlite_query)
			findmas=cursor.fetchall()
			cursor.close()
			answer_text=""
			#fileforflag.dictfordata[str(message.from_user.id)]=""
			if len(findmas)!=0:
				answer_text=answer_text+dictforrightout.dictionary[findmas[0][0]]+"\n"
				for i in findmas:
					answer_text+=i[1]
					answer_text+='\n'
					answer_text+=i[2]
					answer_text+='\n'
					sqlite_connection = sqlite3.connect('sqlite_python.db')
					cursor = sqlite_connection.cursor()
					#print(fileforflag.data)
					sqlite_query='''SELECT TASK_NAME FROM TASK
					WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
					AND DATE= \''''+str(find)+"\' AND TIME = \'"+i[1]+"\';"
					cursor.execute(sqlite_query)
					findtask=cursor.fetchall()
					cursor.close()
					if (len(findtask)!=0):
						answer_text+=findtask[0][0]
						answer_text+='\n'
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
				sqlite_query='''SELECT TASK_NAME FROM TASK
				WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
				AND DATE= \''''+str(find)+"\' AND TIME = \'\';"
				cursor.execute(sqlite_query)
				findtask=cursor.fetchall()
				cursor.close()
				if (len(findtask)!=0):
					answer_text+=findtask[0][0]
					answer_text+='\n'
				markup.add(types.KeyboardButton("записать свои дела"))	
				markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
				bot.send_message(message.from_user.id,answer_text,reply_markup=markup)
			else:
				markup.add(types.KeyboardButton("выбрать другую дату"))
				markup.add(types.KeyboardButton("записать свои дела"))
				markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
				answer_text="занятий в этот день нет)\nможете выбрать другую дату или записать свои собственные дела"
				bot.send_message(message.from_user.id,answer_text,reply_markup=markup)
		else:
			fileforflag.dictforflag[str(message.from_user.id)]=1
			fileforflag.dictfordata[str(message.from_user.id)]=find
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			text = "найдено несколько факультетов! пожалуйста, выберите какой вам нужен в данный момент"
			for t in findmas:
				markup.add (types.KeyboardButton(t[0]))
			markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
			bot.send_message(message.from_user.id, text,reply_markup=markup)
	elif (message.text=="да"):
		fileforflag.dictfortime[str(message.from_user.id)]=""
		fileforflag.dictfordata[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		find=str(datetime.now().day) +".0"+ str(datetime.now().month) + "." +str(datetime.now().year)
		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		fileforflag.dictfordata[str(message.from_user.id)]=find
		sqlite_query='''SELECT FACULTY_NAME FROM FACULTY
		WHERE USERNAME=\''''+ str(message.from_user.id)+"\';"
		cursor.execute(sqlite_query)
		findmas=cursor.fetchall()
		cursor.close()
		if (len(findmas)==1):
			print(findmas[0][0])
			fileforflag.dictforfaculty[str(message.from_user.id)]=findmas[0][0]
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			fileforflag.dictforflag[str(message.from_user.id)]=0
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''SELECT DAY_WEEK,TIME1,SUBJECT_NAME FROM SUBJECT
			WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+findmas[0][0]+'''\'
			AND DATE1= \''''+str(find)+"\';"
			cursor.execute(sqlite_query)
			findmas=cursor.fetchall()
			cursor.close()
			answer_text=""
			if len(findmas)!=0:
				answer_text=answer_text+dictforrightout.dictionary[findmas[0][0]]+"\n"
				for i in findmas:
					answer_text+=i[1]
					answer_text+='\n'
					answer_text+=i[2]
					answer_text+='\n'
					sqlite_connection = sqlite3.connect('sqlite_python.db')
					cursor = sqlite_connection.cursor()
					#print(fileforflag.data)
					sqlite_query='''SELECT TASK_NAME FROM TASK
					WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
					AND DATE= \''''+str(find)+"\' AND TIME = \'"+i[1]+"\';"
					cursor.execute(sqlite_query)
					findtask=cursor.fetchall()
					cursor.close()
					if (len(findtask)!=0):
						answer_text+=findtask[0][0]
						answer_text+='\n'
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
				sqlite_query='''SELECT TASK_NAME FROM TASK
				WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
				AND DATE= \''''+str(find)+"\' AND TIME = \'\';"
				cursor.execute(sqlite_query)
				findtask=cursor.fetchall()
				cursor.close()
				if (len(findtask)!=0):
					answer_text+=findtask[0][0]
					answer_text+='\n'
				markup.add(types.KeyboardButton("записать свои дела"))
				markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
				bot.send_message(message.from_user.id,answer_text,reply_markup=markup)
			else:
				markup.add(types.KeyboardButton("выбрать другую дату"))
				markup.add(types.KeyboardButton("записать свои дела"))
				markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
				answer_text="занятий в этот день нет)\nможете выбрать другую дату или записать свои собственные дела"
				bot.send_message(message.from_user.id,answer_text,reply_markup=markup)
		else:
			fileforflag.dictforflag[str(message.from_user.id)]=1
			fileforflag.dictfordata[str(message.from_user.id)]=find
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			text = "найдено несколько факультетов! пожалуйста, выберите какой вам нужен в данный момент"
			for t in findmas:
				markup.add (types.KeyboardButton(t[0]))
			markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
			bot.send_message(message.from_user.id, text,reply_markup=markup)	

	elif (message.text=="записать свои дела"):
		fileforflag.dictfortime[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		for time in dictforrightout.arraytime:
			markup.add(types.KeyboardButton(time))
		markup.add(types.KeyboardButton("добавить дело без времени"))
		markup.add(types.KeyboardButton("выбрать другую дату"))
		markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id,"выберите время ниже или добавьте свои дела без времени",reply_markup=markup)
	elif (message.text=="добавить дело без времени"):
		fileforflag.dictfortime[str(message.from_user.id)]=""
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		#markup.add(types.KeyboardButton("запишите дела"))
		markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id,"запишите свои дела",reply_markup=markup)		
	elif ((message.text+" ") in dictforrightout.arraytime):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		#markup.add(types.KeyboardButton("запишите дела"))
		fileforflag.dictfortime[str(message.from_user.id)]=message.text+" "
		markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id,"запишите свои дела",reply_markup=markup)
	elif (len(fileforflag.dictfortime[str(message.from_user.id)])!=""):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		print(dictforrightout.arraytime)
		print(message.text)
		print(message.text in dictforrightout.arraytime)

		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		#print(fileforflag.data)
		sqlite_query='''SELECT TASK_NAME FROM TASK
		WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
		AND DATE= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\' AND TIME = \'"+fileforflag.dictfortime[str(message.from_user.id)]+"\';"
		cursor.execute(sqlite_query)
		findtask1=cursor.fetchall()
		cursor.close()

		if (len(findtask1)!=0):
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''UPDATE TASK 
			SET TASK_NAME=\''''+message.text+"\n"+findtask1[0][0]+'''\' WHERE USERNAME =
			\''''+str(message.from_user.id)+'\' AND FACULTY= \''+fileforflag.dictforfaculty[str(message.from_user.id)]+'\' AND DATE=\''+fileforflag.dictfordata[str(message.from_user.id)]+'\' AND TIME = \''+fileforflag.dictfortime[str(message.from_user.id)]+'\';'
			cursor.execute(sqlite_query)
			sqlite_connection.commit()
			print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
			cursor.close()			
		else:	
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''INSERT INTO TASK (DATE,FACULTY,TIME,TASK_NAME,USERNAME) 
			SELECT \''''+ fileforflag.dictfordata[str(message.from_user.id)]+"\',\'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'\',\''+fileforflag.dictfortime[str(message.from_user.id)]+'''\',
			\''''+message.text+'\',\''+str(message.from_user.id)+'''\' WHERE NOT EXISTS (SELECT* FROM TASK WHERE USERNAME =
			\''''+str(message.from_user.id)+'\' AND FACULTY= \''+fileforflag.dictforfaculty[str(message.from_user.id)]+'\' AND DATE=\''+fileforflag.dictfordata[str(message.from_user.id)]+'\' AND TIME = \''+fileforflag.dictfortime[str(message.from_user.id)]+'\');'
			cursor.execute(sqlite_query)
			sqlite_connection.commit()
			print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
			cursor.close()

		sqlite_connection = sqlite3.connect('sqlite_python.db')
		cursor = sqlite_connection.cursor()
		#print(fileforflag.data)
		sqlite_query='''SELECT DAY_WEEK,TIME1,SUBJECT_NAME FROM SUBJECT
		WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
		AND DATE1= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\';"
		cursor.execute(sqlite_query)
		findmas=cursor.fetchall()
		cursor.close()
		answer_text=""
		if len(findmas)!=0:
			answer_text=answer_text+dictforrightout.dictionary[findmas[0][0]]+"\n"
			for i in findmas:
				answer_text+=i[1]
				answer_text+='\n'
				answer_text+=i[2]
				answer_text+='\n'
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
				sqlite_query='''SELECT TASK_NAME FROM TASK
				WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
				AND DATE= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\' AND TIME = \'"+i[1]+"\';"
				cursor.execute(sqlite_query)
				findtask=cursor.fetchall()
				cursor.close()
				if (len(findtask)!=0):
					answer_text+=findtask[0][0]
					answer_text+='\n'
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''SELECT TASK_NAME FROM TASK
			WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
			AND DATE= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\' AND TIME = \'\';"
			cursor.execute(sqlite_query)
			findtask=cursor.fetchall()
			cursor.close()
			if (len(findtask)!=0):
				answer_text+=findtask[0][0]
				answer_text+='\n'
		else:
			for i in dictforrightout.arraytime:
				answer_text+=i
				answer_text+='\n'
				sqlite_connection = sqlite3.connect('sqlite_python.db')
				cursor = sqlite_connection.cursor()
				#print(fileforflag.data)
				sqlite_query='''SELECT TASK_NAME FROM TASK
				WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
				AND DATE= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\' AND TIME = \'"+i+"\';"
				cursor.execute(sqlite_query)
				findtask=cursor.fetchall()
				cursor.close()
				if (len(findtask)!=0):
					answer_text+=findtask[0][0]
					answer_text+='\n'
			sqlite_connection = sqlite3.connect('sqlite_python.db')
			cursor = sqlite_connection.cursor()
			#print(fileforflag.data)
			sqlite_query='''SELECT TASK_NAME FROM TASK
			WHERE USERNAME=\''''+ str(message.from_user.id)+"\' AND FACULTY= \'"+fileforflag.dictforfaculty[str(message.from_user.id)]+'''\'
			AND DATE= \''''+fileforflag.dictfordata[str(message.from_user.id)]+"\' AND TIME = \'\';"
			cursor.execute(sqlite_query)
			findtask=cursor.fetchall()
			cursor.close()
			if (len(findtask)!=0):
				answer_text+=findtask[0][0]
				answer_text+='\n'

		print(answer_text)
		markup.add(types.KeyboardButton("выбрать другую дату"))
		markup.add(types.KeyboardButton("записать свои дела"))
		markup.add(types.KeyboardButton("вернуться в главное меню🔙"))
		bot.send_message(message.from_user.id,answer_text,reply_markup=markup)




	

			

		

if __name__ == "__main__":
	bot.polling(none_stop=True, interval=0)


