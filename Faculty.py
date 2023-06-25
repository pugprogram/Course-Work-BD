import requests
from bs4 import BeautifulSoup
import re 

faculty=""
ListOfFaculty=[]
ListOfCourse=[]
def func_for_delete_space(text):
	a=''
	for i in text:
		if (i!=' ') and (i!='\n'):
			a+=i
	return a
	
#Function for creating connection with bmstu.ru
def get_html(url):
	try:
		result = requests.get(url)
		result.raise_for_status()
		return result.text
	except(requests.RequestException, ValueError):
		print('Server error')
		return False
		
def FindFaculty():
	ListOfFaculty=[]
	url='https://lks.bmstu.ru/schedule/list'
	html=get_html(url)
	soup=BeautifulSoup(html,'html.parser')
	for info in soup.findAll('h4', class_='list-group-item-heading'):
		ListOfFaculty.append(info.text)
	return ListOfFaculty

def ListOfNumFaculty(faculty):
	url='https://lks.bmstu.ru/schedule/list'
	html=get_html(url)
	soup=BeautifulSoup(html,'html.parser')
	find=0
	ListOfNum=[]
	for info in soup.findAll('div', class_='panel panel-default'):
		for info1 in info.findAll('a',class_='btn text-primary'):
			for info2 in info1.findAll('h4'):
				if re.match(faculty,info2.text):
					ListOfNum.append(info2.text)
					find=1
		if (find):
			break
	return ListOfNum
	
def PrintCourse(faculty):
	url='https://lks.bmstu.ru/schedule/list'
	html=get_html(url)
	find=0
	soup=BeautifulSoup(html,'html.parser')
	ListOfNum=[]
	for info in soup.findAll('div', class_='row'):
		for info1 in info.findAll('a',class_='btn btn-primary col-1 rounded schedule-indent'):
			infofind=func_for_delete_space(info1.text)
			if re.match(faculty,infofind):
				ListOfNum.append(infofind)
				find=1
		if (find==1):
			break	
	return ListOfNum
	
def FINDALL(faculty):
	url='https://lks.bmstu.ru/schedule/list'
	html=get_html(url)
	soup=BeautifulSoup(html,'html.parser')
	for info in soup.findAll('div', class_='row'):
		for info1 in info.findAll('a',class_='btn btn-primary col-1 rounded schedule-indent'):
			infofind=func_for_delete_space(info1.text)
			if re.match(faculty,infofind):
				return info1.attrs.get("href")
			
			

					
		
