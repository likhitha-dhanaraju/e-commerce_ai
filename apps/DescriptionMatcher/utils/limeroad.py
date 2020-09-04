import requests
from lxml import html
import json
import re

SYMBOLS = "{}()[].:;+-*/&|<>=~$1234567890 "

class Limeroad():
	def __init__(self,url):
		self.url = url 
		r = requests.get(self.url).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script[@type="application/ld+json"]/text()')
		self.jobj = json.loads(strjson[0])

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

	def get_product_data(self):
		productname = self.jobj['name'].lower().strip().split(' ')
		description = self.jobj['description'].lower()
		words = [word for word in description.strip().split(' ') if any(char not in SYMBOLS for char in word)]
		description_words = self.cleaning_data(words)
		productname = self.cleaning_data(productname)
		data= {
			'product_name':productname,
			'keywords':description_words
				}

		return data

	def image_urls(self):

		image_urls=[]
		for img in jobj['image']:
			if img not in image_urls:
				image_urls.append(img)

		return image_urls

	def pricing(self):
		price = self.jobj['offers']['price']

		return {'pricing':price}

	def availability(self):
		#condition = jobj['offers']['itemCondition'].split('/')[-1]
		availability =  self.jobj['offers']['availability'].split('/')[-1]

		return {'availability':availability}