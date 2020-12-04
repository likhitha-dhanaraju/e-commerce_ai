import requests
from lxml import html
import json
import re
import os

url = 'https://www.bewakoof.com/p/bts-army-boyfriend-t-shirt-for-women'

r = requests.get(url).text
parser = html.fromstring(r)
strjson = parser.xpath('//script[@type="application/ld+json"]')
if len(strjson)>0:
	jobj_1 = json.loads(strjson[1].text)
	jobj_2 = json.loads(strjson[2].text)

def cleaning_data(wordlist):
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

product_name = jobj_1['name'].lower()
brandname = jobj_1['brand'].lower().split('.')[0]
keywords=[]

for num in range(1, len(jobj_2['itemListElement'])):
	keyword = jobj_2['itemListElement'][num]['item']['name'].lower().split(' ')
	for word in keyword:
		if '(' in word:
			continue
		keywords.append(re.sub(r'[^\w]', '', word))
keywords.append(brandname)

keywords = cleaning_data(keywords)
condition = jobj_1['offers']['itemCondition'].split('/')[-1]
availability = jobj_1['offers']['availability'].split('/')[-1].lower()
image_urls=[]
for img in jobj_1['image']:
	if img not in image_urls:
		image_urls.append(img)
pricing = jobj_1['offers']['price']

data={
	'product_name':product_name,
	'keywords':list(set(keywords)),
	'image_urls':image_urls,
	'pricing':pricing,
	'condition':condition,
	'availability':availability
		}

folder_name = url.strip().split('/')[-1]
folder_name = re.sub('/','',folder_name)

folder_path = os.getcwd()

parent_folder = os.path.join(folder_path,'bewakoof_'+folder_name)

if os.path.exists(parent_folder)==False:
	os.mkdir(parent_folder)
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
