import json
from lxml import html
import re
from selenium import webdriver
import time
import os
import requests

url ='https://www.myntra.com/jeans/high-star/high-star-women-black-slim-fit-high-rise-clean-look-stretchable-jeans/7289168/buy'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,
			executable_path='/home/likhitha/.firefox/geckodriver')
driver.maximize_window()
driver.get(url)

content = driver.find_element_by_xpath('/html/body/script[3]').get_attribute('innerText')
content = content.replace('window.__myx = ','')
jobj = json.loads(content)

folder_name = url.strip().split('/')[-3]+'_'+ url.strip().split('/')[-2]

data={}

product_name = jobj['pdpData']['name']

image_urls=[]
for img in jobj['pdpData']['media']['albums'][0]['images']:
	image_urls.append(img['imageURL'])

brandname = jobj['pdpData']['analytics']['brand']

desc = jobj['pdpData']['descriptors']
description = desc[0]['description']+'.'+desc[-1]['description']

keywords= str(jobj['pdpData']['articleAttributes'])
keywords = keywords.replace("'",'').replace('}','').replace('{','')

if jobj['pdpData']['ratings']!=None:
	avg_rating = jobj['pdpData']['ratings']['averageRating']
	data['rating'] = avg_rating

price = jobj['pdpData']['sizes'][0]['sizeSellerData'][0]['mrp']
discount_price = jobj['pdpData']['sizes'][0]['sizeSellerData'][0]['discountedPrice']
		
data['product_name'] = product_name
data['description'] =description
data['keywords']=keywords
data['price']= price
data['discount_price']=discount_price
data['image_urls']=image_urls

folder_path = os.getcwd()

parent_folder = os.path.join(folder_path, 'myntra_'+ folder_name)

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
