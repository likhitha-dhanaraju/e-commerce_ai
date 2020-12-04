from selenium import webdriver
import time
import json
import re
import requests
from lxml import html 
import os

url = 'https://www.flipkart.com/jockey-casual-sleeveless-solid-women-black-top/p/itmf3z5cqtrn49qe?pid=TOPEA8J2YDCT8PEC&lid=LSTTOPEA8J2YDCT8PECGSVONV&marketplace=FLIPKART&srno=b_3_97&otracker=browse&fm=organic&iid=412e2f2e-8863-41d3-8805-cf360943e98d.TOPEA8J2YDCT8PEC.SEARCH&ssid=3ktun3fzv40000001596528895053'

text = requests.get(url).text
parser = html.fromstring(text)
strjson = parser.xpath('//script[@id="is_script"]')[0]
jobj = json.loads(strjson.text.replace(
									'window.__INITIAL_STATE__ = ','').replace('};','}'))

folder_name = url.strip().split('?')[0]
items = folder_name.strip().split('/')
folder_name = items[-3]+'_'+ items[-1]


data={}

name = jobj['pageDataV4']['page']['pageData']['seoData']['schema'][0]
if 'name' in name.keys():
	product_name = name['name'].lower()
else:
	product_name = name['itemListElement'][-1]['item']['name']

description = jobj['pageDataV4']['page']['pageData']['seoData']['seo']['description'].lower()
keywords = jobj['pageDataV4']['page']['pageData']['seoData']['seo']['keywords']
url = jobj['pageDataV4']['page']['pageData']['pageContext']['seo']['webUrl']
availability = jobj['pageDataV4']['page']['pageData']['pageContext']['faAvailable']
marketplace = jobj['pageDataV4']['page']['pageData']['pageContext']['marketplace']
		
if jobj['pageDataV4']['page']['pageData']['pageContext']['pricing'] !=None:
	initial_price = jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['finalPrice']['value']
	discount = jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['prices'][0]['discount']
	final_price = jobj['pageDataV4']['page']['pageData']['pageContext']['pricing']['minPrice']['value']

	data['pricing'] = {
				'initial_price':initial_price,
				'discount':discount,
				'final_price':final_price
			}
if jobj['pageDataV4']['page']['pageData']['pageContext']['rating'] != None:
	avg_rating = jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['average']
	base_rating = jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['base']
	final_rating = avg_rating/base_rating
	rating_breakup = jobj['pageDataV4']['page']['pageData']['pageContext']['rating']['breakup']
		
	data['final_rating'] = final_rating
	data['rating_breakup'] = rating_breakup

brandname = jobj['pageDataV4']['page']['pageData']['pageContext']['brand']
#delivery_time = self.jobj['pageDataV4']['page']['data']['10006'][0]['widget']['data']['deliveryMessages'][0]['value']['dateText']
other_image_urls = jobj['pageDataV4']['page']['data']['10001'][0]['widget']['data']['multimediaComponents']

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

folder_path = os.getcwd()

parent_folder = os.path.join( 'flipkart_'+folder_name)

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

