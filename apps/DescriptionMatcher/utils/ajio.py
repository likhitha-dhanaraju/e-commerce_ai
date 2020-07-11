import requests
import json
from lxml import html
import re

SYMBOLS = "{}()[].,:;+-*/&|<>=~$1234567890"


class Ajio():
	def __init__(self,url):

		self.url = url
		headers = requests.utils.default_headers()
		headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		r = requests.get(self.url,headers=headers).text
		parser = html.fromstring(r)
		
		if 'window.__PRELOADED_STATE__' in parser.xpath('//script')[10].text:
			strjson = parser.xpath('//script')[10]
			self.jobj = json.loads(str(strjson.text).replace("window.__PRELOADED_STATE__ = ","").replace("};","}"))

		elif 'window.__PRELOADED_STATE__' in parser.xpath('//script')[11].text:
			strjson = parser.xpath('//script')[11]
			self.jobj = json.loads(str(strjson.text).replace("window.__PRELOADED_STATE__ = ","").replace("};","}"))

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
		product_name = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['altText'].lower().strip().split(' ')
		keywords =[]
		keywords.append(self.jobj['product']['productDetails']['brickCategory'].lower())
		keywords.append(self.jobj['product']['productDetails']['brickName'].lower())
		keywords.append(self.jobj['product']['productDetails']['brickSubCategory'].lower())
		keywords.append(self.jobj['product']['productDetails']['fnlProductData']['styleType'].lower())
		if 'color' in self.jobj['product']['productDetails']['baseOptions'][0]['selected'].keys():
			keywords.append(self.jobj['product']['productDetails']['baseOptions'][0]['selected']['color'].lower())
		#keywords.append(jobj['product']['productDetails']['fnlProductData']['productGroups'])
		brandname = self.jobj['product']['productDetails']['brandName'].lower()

		keywords.append(brandname)
		keywords = self.cleaning_data(keywords)
		product_name = self.cleaning_data(product_name)
		data={
			'product_name':product_name,
			'keywords':keywords,
		}

		return data

	def pricing(self):
		initial_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['wasPriceData']['value']
		display_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['value']
		discount = round((initial_price - display_price)*100 / initial_price,1)
		final_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['taxInformation']['priceWithTaxes']['value']

		data ={
			'price_data':{
				'initial_price':initial_price,
				'display_price':display_price,
				'discount':discount,
				'final_price':final_price
			},
		}

		return data
	def availability(self):
		avail_number = self.jobj['product']['productDetails']['stock']['stockLevel']
		return {'availability': avail_number}

	def image_urls(self):
		image_urls=[]
		image_urls.append(self.jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['url'])
		for img in jobj['product']['productDetails']['images']:
			url = img['url']
			if '.jpg' not in url:
				continue
			if  img['format'] == 'product' and url not in image_urls:
				image_urls.append(url)

		return image_urls


