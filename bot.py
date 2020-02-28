from seleniumrequests import Chrome
from seleniumrequests import PhantomJS
from seleniumrequests import Firefox
from bs4 import BeautifulSoup as BS
from collections import defaultdict   
from seleniumrequests.request import RequestMixin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup
from w3lib.html import replace_entities
from tabulate import tabulate
import configparser
from html.parser import HTMLParser
from configparser import SafeConfigParser
from cleanco import cleanco
import random, math, os, time, re, html, json
import colorama,html.parser,unicodedata
import datetime, wmi,pickle,calendar
import urllib



from bs4 import BeautifulSoup
import pandas as pd
import regex as re
from pandas import Series,DataFrame
from pandas.io.json import json_normalize


parser = configparser.ConfigParser()
parser.read('config.ini')


base_driver = parser.get('Driver', 'Driver')
driver_selection = {'CHROME':'Chrome(chrome_options=chrome_options)','PHANTHOMJS':'PhantomJS()','PHANTHOM':'PhantomJS("phantomjs.exe")','PHANTHOM.JS':'PhantomJS()','FIREFOX':'Firefox()','FIREFOX()':'Firefox()','CHROME()':'Chrome(chrome_options=chrome_options)','PHANTHOMJS()':'PhantomJS()','PHANTHOM.JS()':'PhantomJS()','PHANTHOM':'PhantomJS()','PHANTHOM()':'PhantomJS()'}



class Browser:
	
	def __init__(self):

		"""Function to Initilize the Driver."""

		try:
			#suspicious block of code
			chrome_options = Options()
			chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36");
			#chrome_options.add_argument("--headless")
			# Headless option helps in running the scrapper without a brower.
			chrome_options.add_argument("--window-size=1366x768")
			chrome_options.add_argument("--disable-logging")
			chrome_options.add_argument("--log-level=3")
			chrome_options.add_argument("--dns-prefetch-disable")
			chrome_options.add_argument('--ignore-certificate-errors')
			chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
			base_driver_selected = driver_selection.get(base_driver.upper())
			self.driver = eval(base_driver_selected)
		except Exception as Initialize_Driver_Exception:
			# This block will be executed if an exception is caught
			print (Initialize_Driver_Exception)
            
            
            
	def Load(self,URL):
	
		"""Function to load an URL in the browser."""
		
		startTime = time.time()
		print('Requesting URL	 :' + URL + '\n')
		time.sleep(1)	
		try:
			self.driver.set_page_load_timeout(200)
			self.driver.get(URL)
			scroll = self.driver.find_element_by_tag_name('body')
			try:
				for i in range(0,10):
					time.sleep(1)
					scroll.send_keys(Keys.PAGE_DOWN)
				for i in range(0,10):	
					time.sleep(1)
					scroll.send_keys(Keys.PAGE_UP)
			except: 
				pass
			time.sleep(random.randint(5,12))
			html = self.driver.page_source
			return html
		
		except TimeoutException as Timeout_Exception:
			Update('0000',Timeout_Exception,'Problem with Browser >> load Module - Timeout_Exception')
			time.sleep(10)
			return "Something unexpected happened and your request could not be completed"
		
		if not time.time()>startTime:
			Utilities.Progress_Bar(startTime-time.time())
		Utilities.Print('Total time taken   : %.2f' %(time.time()-startTime) + '\n')
		Utilities.Print("\n")
        
        
        
	def Request(self,opener,CompanyName,Contact_Name):
	
		"""Function to Load an Google URL in the Browser."""
	
		try:
			url = 'https://www.google.com/search?q=site%3Alinkedin.com%2C+'+str(Contact_Name)+'+,+'+str(CompanyName)
			req = urllib2.Request(url)
			req.add_header('Host', 'www.google.com')
			req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
			req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
			req.add_header('Connection', 'keep-alive')
			req.add_header('Content-Type', 'application/x-www-form-urlencoded')
			resp = opener.open(req,timeout=20)
			return resp.read()
		except:
			return None
        
        
        
	def Input(self,Element,Keys,IsSubmit):
	
		"""Function to fetch the input in text box and click the submit button"""
		
		TextBox = self.driver.find_element_by_id(Element)
		TextBox.clear()
		TextBox.send_keys(Keys)
		if IsSubmit == True:
			TextBox.submit()
			time.sleep(random.randint(15,25))
			html = self.driver.page_source.encode('cp850', errors='replace')
			return html
        
        
        
	def Get_Session(self):
	
		"""Function to open browser using previous saved session"""
	
		for cookie in pickle.load(open("session.pkl", "rb")):
			self.driver.add_cookie(cookie)
            
            
            
	def Save_Session(self):
	
		"""Function to capture current session of the browser"""
		
		pickle.dump(self.driver.get_cookies() , open("session.pkl","wb"))
        
        
        
	def Status(self):

		"""Function to get the status of the Driver"""

		try:
			#suspicious block of code
			self.driver.execute(Command.STATUS)
			return "Alive"

		except (socket.error, httplib.CannotSendRequest):
			# This block will be executed if an exception is caught
			return "Dead"
        
        
        
	def Refresh(self):
		
		"""Function to refresh the driver """

		self.driver.refresh()		
		
	def Close(self):
		
		"""Function to Exit the driver and close the browser"""
		
		self.driver.quit()
        
        
        
def get_details(url,link):
    content=link.Load(url)

    with open('html_content', "a", encoding="utf-8") as r0:
        r0.write(content)
    contacts=get_json('html_content')
    write_excel(contacts) 
    

    
    
def get_json(file):
        file = open(file, "r",encoding="utf-8",errors='ignore')

        con = (file.read())

        soup=BeautifulSoup(con,'html.parser')

        container=soup.find_all('div',{'class':'pv-content profile-view-grid neptune-grid two-column ghost-animate-in'})
        companies=soup.find_all('li',{'class': 'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})
        education=soup.find_all('li',{'class':'pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view'})
    
        for element in container:
            contacts={}
            name=element.find_all('li',{'class':'inline t-24 t-black t-normal break-words'})
            name=name[0].text.strip()
            name=name.split(' ')
            contacts['First_Name']=name[0]
            contacts['Last_Name']=name[1]
            contacts['Experience']=[]
            contacts['Education']=[]
        for company in companies:
            emp={}
            comp=company.find_all('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'})
            emp['Company']=comp[0].text.strip()
            designation=company.find_all('h3',{'class':'t-16 t-black t-bold'})
            emp['Designation']=designation[0].text.strip()
            emp['TimePeriod'] = (company.find_all("h4", {"class": "pv-entity__date-range"}))[0].text.replace('Dates Employed', '').strip() if (company.find_all("h4", {"class": "pv-entity__date-range"}))[0] is not None else ''
            emp['Company_Location']= (company.find_all("h4", {"class": "pv-entity__location"}))[0].text.replace('Location','').strip() if (company.find_all("h4", {"class": "pv-entity__location"}))[0] is not None else ''
            emp['No_of_Years']=(company.find_all("span", {"class": "pv-entity__bullet-item-v2"}))[0].text.strip() if (company.find_all("span", {"class": "pv-entity__bullet-item-v2"}))[0] is not None else ''
            contacts['Experience'].append(emp)
        
        for edu in education:
            educ={}
            school=edu.find_all('h3',{'class':'pv-entity__school-name t-16 t-black t-bold'})
            educ['School']=school[0].text.strip()
            degree=edu.find_all('span',{'class':'pv-entity__comma-item'})
            educ['Degree']=degree[0].text.strip()
            special=edu.find_all('p',{'class':'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'})
            educ['Specialisation']=special[0].text.replace('Field Of Study','').strip()
            contacts['Education'].append(educ)

        return(contacts)
    
    
    
def write_excel(contacts):
    print(contacts)
    with open('test.json', 'w') as fp:
        json.dump(contacts, fp)
        
    df=pd.DataFrame.from_dict(contacts, orient='index').transpose()
    print(df)
    df=pd.read_json('test.json')
    df2 = json_normalize(df['Experience'])
    df3=json_normalize(df['Education'])
    df1=df.drop(['Experience', 'Education'], axis = 1)
    frames = [df1, df2, df3]
    dff=pd.concat(frames,axis=1)
    dff=extract_years(dff)
    dff.to_excel('test.xlsx')
    
    


link=Browser()

link.Load('https://www.linkedin.com/login')

link.Input('username','9840509861',False)

link.Input('password','test@123',True)

urls=['https://www.linkedin.com/in/vishal-vijayaraghavan-007baa17/']

for url in urls:
    get_details(url,link)     
    

