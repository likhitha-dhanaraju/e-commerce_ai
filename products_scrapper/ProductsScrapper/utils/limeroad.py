import json
import requests
from lxml import html
import re
import os
import numpy as np 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

SYMBOLS = "{}()[].:;+-*/&|<>=~$1234567890 "

class UrlsList():
	def __init__(self,url):
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		self.driver  =webdriver.Firefox(options=options, executable_path='/home/likhitha/.firefox/geckodriver')
		self.driver.get(url)
		self.driver.maximize_window()
		total_count = self.driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[1]/div/div/div").get_attribute('innerText')
		self.total_count = int(re.sub(r'[^\d]','',total_count))

		print("Total count", self.total_count)

	def list_of_products(self,filename):
		urls_list=[]
		i=1

		count=0
		flag = 0
		while len(urls_list)<self.total_count:
			time.sleep(1)
			try:
				f = open(filename,'a+')
				content = self.driver.find_element_by_css_selector('div.prdC:nth-child('+str(i)+') > a:nth-child(1)')	
				_url_ = content.get_attribute('href')
				print(_url_)
				urls_list.append(_url_)
				f.write(_url_+'\n')
				count=0
				f.close()

			except NoSuchElementException:
				print("No URL")
				count+=1
			
			if i%6 == 0:
				content.send_keys(Keys.PAGE_DOWN)
				print("Scrolling down!")

			if count>10:
				content.send_keys(Keys.PAGE_UP)
				print("Scrolling up!")
				flag+=1
				count = 0

			if flag > 10:
				break

			i+=1
			print(len(urls_list))
		

		if len(urls_list)== self.total_count:
			print("All URLs were successfully retreived!")

		else:
			print("Some URLs are missing")


class Limeroad():
	def __init__(self,url):
		self.url = url 
		r = requests.get(self.url).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script[@type="application/ld+json"]/text()')[0]
		if strjson!=[]:
			strjson = re.sub("\n"," ",strjson)
			strjson = re.sub("\t"," ",strjson)
			strjson = re.sub(r"\\,","",strjson)
			strjson = re.sub(r"\\ ","",strjson)
			strjson = re.sub(r'" ','\" ',strjson)
			self.jobj = json.loads(strjson)

	def cleaning_data(self,wordlist):
		final_keywords=[]
		for wordd in wordlist:
			for word in wordd.strip().split(' '):
				word_ = re.sub(r'\d',' ', word)
				word_ = re.sub(r'[^\w]', ' ', word_)
				word_ = word_.strip().split(' ')
				for i in word_:
					if i!='':
						final_keywords.append(i)
		return final_keywords

	def product_data(self, folder_path):
		
		folder_name = self.url.strip().split('?')[0].strip().split('/')[-1]

		product_name = self.jobj['name']
		description = self.jobj['description'].lower()
		#words = [word for word in description.strip().split(' ') if any(char not in SYMBOLS for char in word)]
		#description_words = self.cleaning_data(words)
		price = self.jobj['offers']['price']
		availability =  self.jobj['offers']['availability'].split('/')[-1]
		condition = self.jobj['offers']['itemCondition'].split('/')[-1]
		marketplace = self.jobj['offers']['seller']['name'].split(' ')[0]

		image_urls=[]
		for img in self.jobj['image']:
			if img not in image_urls:
				image_urls.append(img)
		data= {
			'product_name':product_name,
			'keywords':description,
			'image_urls':image_urls,
			'pricing':price,
			'condition':condition,
			'availability':availability
				}	

		parent_folder = os.path.join(folder_path,'limeroad_'+folder_name)

		if os.path.exists(parent_folder)==False:
			os.mkdir(parent_folder)


		product_name = re.sub(r'/','',product_name)

		json_file = os.path.join(parent_folder, product_name+'.json')

		if os.path.exists(json_file)==False:
			with open(json_file,'w') as file:
				json.dump(data,file)
				file.close()

		for val,image_url in enumerate(image_urls):
				image_name = os.path.join(parent_folder,product_name+'_'+'image_'+str(val)+'_'+'.jpg')
				if os.path.exists(image_name)==False:
					with open(image_name,'wb') as image:
						img_r = requests.get(image_url,stream=True)
						for block in img_r.iter_content(1024):
							if not block:
								break
							image.write(block)
