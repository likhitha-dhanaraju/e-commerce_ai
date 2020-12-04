from selenium import webdriver
import time
import json
import re
import requests
from lxml import html 
import os

class UrlsList():
	def __init__(self,url):
		self.base_url = url
		self.add_page = '&page='
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		self.driver = webdriver.Firefox(options=options,
								 executable_path='/home/likhitha/.firefox/geckodriver')
		self.driver.get(url)
		self.driver.maximize_window()
	
		self.number_of_pages = 26

		print("Total count",self.total_count)
		print("Number of pages",self.number_of_pages)

	def list_of_products(self,filename):
		urls_list=[]
		SCROLL_TIME = 2

		f=open(filename, 'w')
		count=1

		for page in range(1, self.number_of_pages):
			print("Page number",page)
			url = self.base_url + self.add_page+str(page)
			self.driver.get(url)
			time.sleep(SCROLL_TIME)
			self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
			time.sleep(SCROLL_TIME)

			for num1 in range(2,12):
				xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div['+str(num1)+']'
				    
				for num2 in range(1,5):
					try:
						sub_xpath =xpath+ '/div/div['+str(num2)+']/div/a'
						content = self.driver.find_elements_by_xpath(sub_xpath)
						_url_ = content[0].get_attribute('href')
						print(count, _url_+'\n')
						urls_list.append(_url_)
						f.write(_url_+'\n')
						count+=1
					except IndexError:
						print("Skipping few items")

		f.close()

		if len(urls_list)==self.total_count:
			print("All URLs are retreived")
		else:
			print("Some URLs are missing")

class Flipkart():
	def __init__(self,url):
		text = requests.get(url).text
		parser = html.fromstring(text)
		strjson = parser.xpath('//script[@id="is_script"]')[0]
		self.jobj = json.loads(strjson.text.replace(
						'window.__INITIAL_STATE__ = ','').replace('};','}'))

		folder_name = url.strip().split('?')[0]
		items = folder_name.strip().split('/')
		self.folder_name = items[-3]+'_'+ items[-1]

	def product_data(self, folder_path):

		data={}


		name = self.jobj['pageDataV4']['page']['pageData']['seoData']['schema'][0]
		if 'name' in name.keys():
			product_name = name['name'].lower()
		else:
			product_name = name['itemListElement'][-1]['item']['name']
		description = self.jobj['pageDataV4']['page']['pageData']['seoData']['seo']['description'].lower()
		keywords = self.jobj['pageDataV4']['page']['pageData']['seoData']['seo']['keywords']
		url = self.jobj['pageDataV4']['page']['pageData']['pageContext']['seo']['webUrl']
		availability = self.jobj['pageDataV4']['page']['pageData']['pageContext']['faAvailable']
		marketplace = self.jobj['pageDataV4']['page']['pageData']['pageContext']['marketplace']
		
		if self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing'] !=None:
			initial_price = self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['finalPrice']['value']
			discount = self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['prices'][0]['discount']
			final_price = self.jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['minPrice']['value']

			data['pricing'] = {
						'initial_price':initial_price,
						'discount':discount,
						'final_price':final_price
					}

		if self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating'] != None:
			avg_rating = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['average']
			base_rating = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['base']
			final_rating = avg_rating/base_rating
			rating_breakup = self.jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['breakup']
			
			data['final_rating'] = final_rating
			data['rating_breakup'] = rating_breakup

		brandname = self.jobj['pageDataV4']['page']['pageData']['pageContext']['brand']
		#delivery_time = self.jobj['pageDataV4']['page']['data']['10006'][0]['widget']['data']['deliveryMessages'][0]['value']['dateText']
		other_image_urls = self.jobj['pageDataV4']['page']['data']['10001'][0]['widget']['data']['multimediaComponents']

		image_width = '710'
		image_height = '710'
		quality = '100'

		image_urls = []

		for val in other_image_urls:
			image_urls.append(val['value']['url'].replace('{@height}',image_height).replace('{@width}',image_width).replace('{@quality}',quality))

		data['product_name'] =product_name
		data['description']= description
		data['keywords']=keywords
		data['availability']=availability
		data['marketplace'] = marketplace
		data['brandname']=brandname
		data['image_urls']=image_urls

		parent_folder = os.path.join(folder_path, 'flipkart_'+self.folder_name)

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

