import os
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))
SYMBOLS = "{}()[].,:;+-*/&|<>=~$1234567890"

class MRFinder():
	def __init__(self,url):
		self.url = url
		self.market_place = str(self.url.strip().split('.com')[0]).strip().split('.')[-1]

	def choosing(self):
		if self.market_place == 'flipkart':
			from .flipkart import Flipkart 
			product_data = Flipkart(self.url).get_product_data()
			product_data['keywords']+= [i for i in product_data['keywords'] if i not in STOPWORDS]
			product_data['keywords'] = sorted(product_data['keywords'])
			return product_data

		elif self.market_place == 'ajio':
			from .ajio import Ajio 
			product_data = Ajio(self.url).get_product_data()
			product_data['keywords'] = sorted(product_data['keywords'])
			return product_data

		elif self.market_place == 'limeroad':
			from .limeroad import Limeroad 
			product_data = Limeroad(self.url).get_product_data()
			product_data['keywords']= [i for i in product_data['keywords'] if i not in STOPWORDS]
			return product_data

		elif self.market_place == 'bewakoof':
			from .bewakoof import Bewakoof 
			product_data = Bewakoof(self.url).get_product_data()
			product_data['keywords'] = sorted(product_data['keywords'])
			return product_data



		else:
			raise ValueError("Enter a valid url from the following market places: Flipkart, Ajio, Bewakoof, Limeroad")
