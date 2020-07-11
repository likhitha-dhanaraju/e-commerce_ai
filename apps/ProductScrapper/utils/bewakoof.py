import json
import requests
from lxml import html
import re
import os
import numpy as np 
from selenium import webdriver
import time

class UrlsList():
	def __init__(self,url):
		self.url = url
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		self.driver = webdriver.Firefox(options=options,
			executable_path='/home/likhitha/.firefox/geckodriver')
		self.driver.get(url)
		self.driver.maximize_window()

		total_content = self.driver.find_element_by_css_selector('.headingInner > span:nth-child(2)')
		total_count = total_content.get_attribute('innerText')
		self.total_count = int(re.sub(r'[^\d]','',total_count))
		print("total_count",self.total_count)

	def list_of_products(self, filename):
		SCROLL_TIME=2
		STEP=2500
		start_length = 0
		end_length = STEP
		i=0

		urls_list=[]

		
		f= open(filename,'a+')

		while i<self.total_count:
			self.driver.execute_script("window.scrollTo("+str(start_length)+","+str(end_length)+")")
			time.sleep(SCROLL_TIME)

			start_length+=STEP
			end_length+=STEP

			id_name ='testProductcard_'+str(i+1)
			content = self.driver.find_element_by_id(id_name).find_element_by_xpath('a')
			i+=1
			_url_= content.get_attribute('href')
			print(_url_)
			urls_list.append(_url_)
			f.write(_url_+'\n')
		f.close()

		print(len(list(set(urls_list))))

		if len(urls_list)==self.total_count:
			print("All URLs are extracted.")
		else:
			print("Some URLs are missing.")

		
class Bewakoof():
	def __init__(self,url):

		self.url = url
		r = requests.get(self.url).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script[@type="application/ld+json"]')
		if len(strjson)>0:
			self.jobj_1 = json.loads(strjson[1].text)
			self.jobj_2 = json.loads(strjson[2].text)

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

	def product_data(self,folder_path):
		product_name = self.jobj_1['name'].lower()
		brandname = self.jobj_1['brand'].lower().split('.')[0]
		keywords=[]
		for num in range(1, len(self.jobj_2['itemListElement'])):
			keyword = self.jobj_2['itemListElement'][num]['item']['name'].lower().split(' ')
			for word in keyword:
				if '(' in word:
					continue
				keywords.append(re.sub(r'[^\w]', '', word))
		keywords.append(brandname)

		keywords = self.cleaning_data(keywords)
		condition = self.jobj_1['offers']['itemCondition'].split('/')[-1]
		availability =  self.jobj_1['offers']['availability'].split('/')[-1].lower()
		image_urls=[]
		for img in self.jobj_1['image']:
			if img not in image_urls:
				image_urls.append(img)

		pricing = self.jobj_1['offers']['price']

		data={
			'product_name':product_name,
			'keywords':list(set(keywords)),
			'image_urls':image_urls,
			'pricing':pricing,
			'condition':condition,
			'availability':availability
				}

		folder_name = self.url.strip().split('/')[-1]
		folder_name = re.sub('/','',folder_name)
		parent_folder = os.path.join(folder_path,'bewakoof_'+folder_name)

		if os.path.exists(parent_folder)==False:
			os.mkdir(parent_folder)
		json_file = os.path.join(parent_folder,product_name+'.json')
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