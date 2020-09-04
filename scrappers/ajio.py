import requests
import json
from lxml import html

url ='https://www.ajio.com/purys-polka-dot-shirt/p/461064729_green'
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

r = requests.get(url,headers=headers).text

parser = html.fromstring(r)

strjson = parser.xpath('//script')[11]

jobj = json.loads(str(strjson.text).replace("window.__PRELOADED_STATE__ = ","").replace("};","}"))

avail_number = jobj['product']['productDetails']['stock']['stockLevel']
colour= jobj['product']['productDetails']['baseOptions'][0]['selected']['color']
product_name = jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['altText']

image_urls=[]
image_urls.append(jobj['product']['productDetails']['baseOptions'][0]['selected']['modelImage']['url'])

initial_price = jobj['product']['productDetails']['baseOptions'][0]['selected']['wasPriceData']['value']
display_price = jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['value']

discount = round((initial_price - display_price)*100 / initial_price,1)

final_price = jobj['product']['productDetails']['baseOptions'][0]['selected']['priceData']['taxInformation']['priceWithTaxes']['value']

keywords =[]
keywords.append(jobj['product']['productDetails']['brickCategory'])
keywords.append(jobj['product']['productDetails']['brickName'])
keywords.append(jobj['product']['productDetails']['brickSubCategory'])
keywords.append(jobj['product']['productDetails']['fnlProductData']['styleType'])
#keywords.append(jobj['product']['productDetails']['fnlProductData']['productGroups'])

brandname = jobj['product']['productDetails']['brandName']

for img in jobj['product']['productDetails']['images']:
	url = img['url']
	if '.jpg' not in url:
		continue
	if  img['format'] == 'product' and url not in image_urls:
		image_urls.append(url)


filename = 'AJIO_'+product_name+'.json'

with open(filename,'w') as file:
	final_dict={
		'product_name':product_name,
		'brandname':brandname,
		'colour':colour,
		'availability_number':avail_number,
		'price_data':{
				'initial_price':initial_price,
				'display_price':display_price,
				'discount':discount,
				'final_price':final_price
		},
		'keywords':keywords,
		'image_urls':image_urls
	}
	json.dump(final_dict,file)

	file.close()
