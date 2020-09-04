import json
import requests
from lxml import html
import re
import os
import numpy as np

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
		print("total_count",total_count)


	def list_of_products(self,filename):
		SCROLL_TIME=2
		STEP=2500
		start_length = 0
		end_length = STEP
		i=0

		urls_list=[]

		f = open(filename,'a+')

		while len(urls_list)<self.total_items:
			print("Scrolling to {}".format(end_length))
			self.driver.execute_script("window.scrollTo("+str(start_length)+","+str(end_length)+")")
			time.sleep(SCROLL_TIME)

			start_length+=STEP
			end_length+=STEP

			content = self.driver.find_elements_by_xpath("//div[@class='items']/div/div/div/a")
			#print("Extracting urls...")
			for item in content:
				#time.sleep(2)
				_url_ = item.get_attribute('href')
				urls_list.append(_url_)
			urls_list = list(set(urls_list))
			print(len(urls_list))
		all_urls=""
		for url in urls_list:
			all_urls+=url+'\n'

		f.write(all_urls)
		f.close()

		if len(urls_list)== total_items:
			print("All URLs were successfully retreived!")

		else:
			print("Some URLs are missing")


class Ajio():
	def __init__(self,url):

		self.url = url
		headers = requests.utils.default_headers()
		headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		r = requests.get(self.url,headers=headers).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script')[11]
		self.jobj = json.loads(strjson.text.replace("window.__PRELOADED_STATE__ = ","").replace("};","}"))

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
			folder_name = self.url.strip().split('/')[-1]

		#if os.path.exists(folder_name)==False:

			product_name = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['altText'].lower()
			keywords =[]
			keywords.append(self.jobj['product']['productDetails']['brickCategory'].lower())
			keywords.append(self.jobj['product']['productDetails']['brickName'].lower())
			keywords.append(self.jobj['product']['productDetails']['brickSubCategory'].lower())
			if 'styleType' in self.jobj['product']['productDetails']['fnlProductData'].keys():
				keywords.append(self.jobj['product']['productDetails']['fnlProductData']['styleType'].lower())
			if 'color' in self.jobj['product']['productDetails']['baseOptions'][0]['selected'].keys():
				keywords.append(self.jobj['product']['productDetails']['baseOptions'][0]['selected']['color'].lower())
			#keywords.append(jobj['product']['productDetails']['fnlProductData']['productGroups'])
			brandname = self.jobj['product']['productDetails']['brandName'].lower()

			keywords.append(brandname)
			keywords = self.cleaning_data(keywords)

			initial_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['wasPriceData']['value']
			display_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['value']
			discount = round((initial_price - display_price)*100 / initial_price,1)
			#final_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['taxInformation']['priceWithTaxes']['value']
			avail_number = self.jobj['product']['productDetails']['stock']['stockLevel']
			image_urls=[]
			image_urls.append(self.jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['url'])
			for img in self.jobj['product']['productDetails']['images']:
				url = img['url']
				if '.jpg' not in url:
					continue
				if  img['format'] == 'product' and url not in image_urls:
					image_urls.append(url)

			data ={
				'product_name':product_name,
				'keywords':keywords,
				'price_data':{
					'initial_price':initial_price,
					'display_price':display_price,
					'discount':discount
				},
				'availability': avail_number,
				'image_urls':image_urls
			}
			folder_name = self.url.strip().split('/')[-1]
			parent_folder = os.path.join(folder_path,'ajio_'+folder_name)

			if os.path.exists(parent_folder)==False:
				os.mkdir(parent_folder)

			product_name = re.sub(r'/','',product_name)

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
