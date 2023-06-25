import requests
from bs4 import BeautifulSoup

#faculty=["AK","БМТ","ИБМ","ИСОТ","ИУ","Л","МТ","ОЭ","ПС","РК","РКТ","РЛ","РТ", "СГН", "СМ", "ФН", "Э", "ЮР"]

def get_html(url):
	try:
		result = requests.get(url)
		result.raise_for_status()
		return result.text
	except(requests.RequestException, ValueError):
		print('Server error')
		return False
		
def FindShedule(url):	
	array_chislitel=[]
	array_znamenatel=[]
	url='https://lks.bmstu.ru'+url	
	html=get_html(url)
	soup=BeautifulSoup(html,'html.parser')

	for info in soup.findAll('table', class_='table table-bordered text-center table-responsive'):
		day_of_week=""
		time=""
		subject=""
		day_of_week=info.find('strong').text
		for info1 in info.find_all('tr'):
			time=info1.find('td',attrs={'class':'bg-grey text-nowrap'})
			if time!=None:
				both=info1.find('td',attrs={'colspan':'2'})
				if (both!=None):
					subject=both.find("span")
				else:
					subject=info1.find('td',attrs={'class':'text-info-bold'})		
					
				
				subject=subject.text
				array_chislitel.append([day_of_week,time.text,subject])
	for info in soup.findAll('table', class_='table table-bordered text-center table-responsive'):
		day_of_week=""
		time=""
		subject=""
		day_of_week=info.find('strong').text
		for info1 in info.find_all('tr'):
			time=info1.find('td',attrs={'class':'bg-grey text-nowrap'})
			if time!=None:
				both=info1.find('td',attrs={'colspan':'2'})
				if (both!=None):
					subject=both.find("span")
				else:
					subject=info1.find('td',attrs={'class':'text-primary'})		
					
				
				subject=subject.text
				array_znamenatel.append([day_of_week,time.text,subject])
			

	return array_chislitel,array_znamenatel
		 	
	
		
