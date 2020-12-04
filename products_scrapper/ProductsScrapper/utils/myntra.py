import json
from lxml import html
import re
from selenium import webdriver
import time
import os
import requests

class UrlsList():
	def __init__(self,url):
		self.base_url = url
		self.add_page='?p='

		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')

		self.driver = webdriver.Firefox(options=options,
					executable_path='/home/likhitha/.firefox/geckodriver')
		self.driver.get(url)
		self.driver.maximize_window()

		total_count = self.driver.find_element_by_css_selector('.title-count').get_attribute('innerText')
		self.total_count = int(re.sub(r'[^\d]','',total_count))

		self.num_pages = int(total_count/50)+2

		print("Total count",total_count)
		print("Number of pages",self.num_pages)

	def list_of_products(self,filename):
		urls_list=[]
		SCROLL_TIME = 2

		f = open(filename,'w')

		count=1
		for num1 in range(1,self.num_pages):
			self.driver.get(self.base_url+self.add_page+str(num1))
			self.driver.execute_script('window.scrollTo(0,5000)')

			time.sleep(SCROLL_TIME)

			for num2 in range(1,51):
				_url_ = self.driver.find_element_by_css_selector(
					'li.product-base:nth-child('+str(num2)+') > a:nth-child(2)').get_attribute('href')
				print(count, _url_)
				count+=1
				urls_list.append(_url_)
				f.write(_url_+'\n')

		f.close()

		if len(urls_list) == self.total_count:
			print("All URLs are retrieved")
		else:
			print("Some URLs are missing")

class Myntra():
	def __init__(self,url):
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		driver = webdriver.Firefox(options=options,
			executable_path='/home/likhitha/.firefox/geckodriver')
		driver.maximize_window()
		driver.get(url)

		content = driver.find_element_by_xpath('/html/body/script[3]').get_attribute('innerText')
		content = content.replace('window.__myx = ','')
		self.jobj = json.loads(content)

		self.folder_name = url.strip().split('/')[-3]+'_'+ url.strip().split('/')[-2]

	def product_data(self,folder_path):

		data={}

		product_name = self.jobj['pdpData']['name']

		image_urls=[]
		for img in self.jobj['pdpData']['media']['albums'][0]['images']:
			image_urls.append(img['imageURL'])

		brandname = self.jobj['pdpData']['analytics']['brand']

		desc = self.jobj['pdpData']['descriptors']
		description = desc[0]['description']+'.'+desc[-1]['description']

		keywords= str(self.jobj['pdpData']['articleAttributes'])
		keywords = keywords.replace("'",'').replace('}','').replace('{','')

		if self.jobj['pdpData']['ratings']!=None:
			avg_rating = self.jobj['pdpData']['ratings']['averageRating']
			data['rating'] = avg_rating

		price = self.jobj['pdpData']['sizes'][0]['sizeSellerData'][0]['mrp']
		discount_price = self.jobj['pdpData']['sizes'][0]['sizeSellerData'][0]['discountedPrice']

		
		data['product_name'] = product_name
		data['description'] =description
		data['keywords']=keywords
		data['price']= price
		data['discount_price']=discount_price
		data['image_urls']=image_urls

		parent_folder = os.path.join(folder_path, 'myntra_'+self.folder_name)
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