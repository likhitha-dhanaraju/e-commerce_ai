import json
import requests
from lxml import html
import re 

SYMBOLS = "{}()[].,:;+-*/&|<>=~$1234567890"

class Flipkart():
	def __init__(self,url):
		self.url = url
		text = requests.get(url).text

		parser = html.fromstring(text)
		strjson = parser.xpath('//script[@id="is_script"]')[0]

		self.jobj = json.loads(strjson.text.replace(
		'window.__INITIAL_STATE__ = ','').replace('};','}'))

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
		product_name = self.jobj['pageDataV4']['page']['pageData']['seoData']['schema'][-1]['itemListElement'][-1]['item']['name'].lower().strip().split(' ')

		if 'keywords' in self.jobj['pageDataV4']['page']['pageData']['seoData']['seo'].keys():
			keywords = self.jobj['pageDataV4']['page']['pageData']['seoData']['seo']['keywords'].lower().strip().split(' ')
		else:
			description = self.jobj['pageDataV4']['page']['pageData']['seoData']['seo']['description'].lower().strip().split('.')[0]
			keywords = [word for word in description.strip().split(' ') if any(char not in SYMBOLS for char in word)]
			
		product_name = self.cleaning_data(product_name)
		keywords= self.cleaning_data(keywords)
		data = {
				'product_name':product_name,
				'keywords':keywords,
		}
		return data

	def image_urls(self):
		all_image_urls = self.jobj['pageDataV4']['page']['data']['10001'][0]['widget']['data']['multimediaComponents']

		image_width = '710'
		image_height = '710'
		quality = '100'

		image_urls = []

		for val in all_image_urls:
			image_urls.append(val['value']['url'].replace('{@height}',image_height).replace('{@width}',image_width).replace('{@quality}',quality))

		return image_urls

	def product_availability(self):

		availability = self.jobj['pageDataV4']['page']['pageData']['pageContext']['faAvailable'].lower()
		delivery_time = self.jobj['pageDataV4']['page']['data']['10006'][0]['widget']['data']['deliveryMessages'][0]['value']['dateText']

		data = {
				'availability':availability,
				'delivery_time':delivery_time
		}
		return data

	def pricing(self):

		initial_price = self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['prices'][0]['value']
		discount = self.self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['totalDiscount']
		final_price = self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['prices'][1]['value']

		data = {
				'pricing':{
					'initial_price':initial_price,
					'discount':discount,
					'final_price':final_price
						},
				}

		return data


	def rating(self):
		avg_rating = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['average']
		base_rating = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['base']
		final_rating = avg_rating/base_rating

		rating_breakup = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['breakup']
		
		data = {
				'final_rating':final_rating,
				'rating_breakup':rating_breakup,
		}

		return data
