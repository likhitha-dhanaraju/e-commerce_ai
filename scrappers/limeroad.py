import requests
from lxml import html
import json

url = 'https://www.limeroad.com/blue-cotton-fosh-p16823095?imgIdx=0&reference_story_id=5eb12fb9fd1d3c05e1f12891'

r = requests.get(url).text

parser = html.fromstring(r)

strjson = parser.xpath('//script[@type="application/ld+json"]/text()')
jobj = json.loads(strjson[0])

productname = jobj['name']
image_urls=[]
for img in jobj['image']:
	if img not in image_urls:
		image_urls.append(img)

description = jobj['description']
brandname = jobj['brand']['name']
price = jobj['offers']['price']
condition = jobj['offers']['itemCondition'].split('/')[-1]
availability =  jobj['offers']['availability'].split('/')[-1]

filename = 'Limeroad_'+productname+'.json'

with open(filename,'w') as file:
	final_dict = {
			'product_name': productname,
			'brand_name':brandname,
			'desciption':description,
			'price':price,
			'condition': condition,
			'availability':availability,
			'image_urls':image_urls,

	}

	json.dump(final_dict,file)
	file.close()