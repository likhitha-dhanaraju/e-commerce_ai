import requests
from lxml import html
import json
import re
import os

url = 'https://www.limeroad.com/blue-cotton-fosh-p16823095?imgIdx=0&reference_story_id=5eb12fb9fd1d3c05e1f12891'

r = requests.get(url).text
parser = html.fromstring(r)
strjson = parser.xpath('//script[@type="application/ld+json"]/text()')[0]

if strjson!=[]:
	strjson = re.sub("\n"," ",strjson)
	strjson = re.sub("\t"," ",strjson)
	strjson = re.sub(r"\\,","",strjson)
	strjson = re.sub(r"\\ ","",strjson)
	strjson = re.sub(r'" ','\" ',strjson)
	jobj = json.loads(strjson)

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

		
folder_name = url.strip().split('?')[0].strip().split('/')[-1]

product_name = jobj['name']
description = jobj['description'].lower()
price = jobj['offers']['price']
availability =  jobj['offers']['availability'].split('/')[-1]
condition = jobj['offers']['itemCondition'].split('/')[-1]
marketplace = jobj['offers']['seller']['name'].split(' ')[0]

image_urls=[]
for img in jobj['image']:
	if img not in image_urls:
		image_urls.append(img)
data= {
	'product_name':product_name,
	'keywords':description,
	'image_urls':image_urls,
	'pricing':price,
	'condition':condition,
	'availability':availability
		}	

folder_path = os.getcwd()
parent_folder = os.path.join(folder_path,'limeroad_'+folder_name)

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