import requests
from lxml import html
import json
import re

class Bewakoof():
	def __init__(self,url):

		self.url = url

		r = requests.get(self.url).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script[@type="application/ld+json"]')
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

	def get_product_data(self):
		product_name = self.jobj_1['name'].lower().strip().split(' ')
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
		product_name = self.cleaning_data(product_name)
		data={
			'product_name':product_name,
			'keywords':list(set(keywords))
				}

		return data

	def image_urls(self):
		image_urls=[]
		for img in self.jobj_1['image']:
			if img not in image_urls:
				image_urls.append(img)

		return image_urls

	def availability(self):
		#condition = self.jobj_1['offers']['itemCondition'].split('/')[-1]
		availability =  self.jobj_1['offers']['availability'].split('/')[-1].lower()

		return {'availability':availability}

	def pricing(self):
		price = self.jobj_1['offers']['price']

		return {'pricing':price}