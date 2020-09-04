import requests
from lxml import html
import json

url = 'https://www.bewakoof.com/p/bts-army-boyfriend-t-shirt-for-women'

r = requests.get(url).text

parser = html.fromstring(r)
strjson = parser.xpath('//script[@type="application/ld+json"]')

jobj_1 = json.loads(strjson[1].text)

product_name = jobj_1['name']
image_urls=[]
for img in jobj_1['image']:
	if img not in image_urls:
		image_urls.append(img)

brandname = jobj_1['brand']
marketplace = jobj_1['offers']['seller']['name'].split(' ')[0]

price = jobj_1['offers']['price']
condition = jobj_1['offers']['itemCondition'].split('/')[-1]
availability =  jobj_1['offers']['availability'].split('/')[-1]

jobj_2 = json.loads(strjson[2].text)

keywords=[]
for num in range(1, len(jobj_2['itemListElement'])):
	keywords.append(jobj_2['itemListElement'][num]['item']['name'])

filename = marketplace+'_'+product_name+'.json'

with open(filename,'w') as file:
	final_dict = {
			'product_name': product_name,
			'price':price,
			'condition': condition,
			'availability':availability,
			'price':price,
			'image_urls':image_urls,
			'keywords':keywords
	}

	json.dump(final_dict,file)
	file.close()