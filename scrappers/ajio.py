import requests
import json
from lxml import html
import re
import os

url ='https://www.ajio.com/purys-polka-dot-shirt/p/461064729_green'

headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
r = requests.get(url,headers=headers).text
parser = html.fromstring(r)

if 'window.__PRELOADED_STATE__' in parser.xpath('//script')[11].text:
	strjson = parser.xpath('//script')[11]
else:
	strjson = parser.xpath('//script')[10]

jobj = json.loads(strjson.text.replace("window.__PRELOADED_STATE__ = ","").replace("};","}"))

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

folder_path = os.getcwd()
folder_name = url.strip().split('/')[-1]

if type(jobj['product']['productDetails'])!=str:
	
	if 'errors' not in jobj['product']['productDetails'].keys():
	
		product_name = jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['altText'].lower()
		keywords =[]
		keywords.append(jobj['product']['productDetails']['brickCategory'].lower())
		keywords.append(jobj['product']['productDetails']['brickName'].lower())
		keywords.append(jobj['product']['productDetails']['brickSubCategory'].lower())
		if 'styleType' in jobj['product']['productDetails']['fnlProductData'].keys():
			keywords.append(jobj['product']['productDetails']['fnlProductData']['styleType'].lower())
		if 'color' in jobj['product']['productDetails']['baseOptions'][0]['selected'].keys():
			keywords.append(jobj['product']['productDetails']['baseOptions'][0]['selected']['color'].lower())

		brandname = jobj['product']['productDetails']['brandName'].lower()

		keywords.append(brandname)
		keywords = cleaning_data(keywords)

		initial_price = jobj['product']['productDetails']['baseOptions'][0]['selected']['wasPriceData']['value']
		display_price = jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['value']
		discount = round((initial_price - display_price)*100 / initial_price,1)
		#final_price = self.jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['taxInformation']['priceWithTaxes']['value']
		avail_number = jobj['product']['productDetails']['stock']['stockLevel']
		image_urls=[]
		image_urls.append(jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['url'])
		for img in jobj['product']['productDetails']['images']:
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
	else:
		print("Product not found!")
