import os

def WebsiteMatcher(url):
	if 'bewakoof' in url:
		from ..utils.bewakoof import UrlsList, Bewakoof
	
		folder_path='bewakoof_products'
		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)
		category = url.strip().split('/')[-1]
		filename = "bewakoof_"+category+'.txt'

		if os.path.exists(filename)!=True:
			UrlsList(url).list_of_products(filename)

		f= open(filename,'r')
		product_urls = f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		for i,url in enumerate(products):
			print(i+1,url)
			Bewakoof(url).product_data(folder_path)

		if len(os.listdir(folder_path)) == len(product_urls):
			return True
		else:
			return False

	elif 'ajio' in url:
		from ..utils.ajio import UrlsList, Ajio
		
		folder_path='ajio_products'
		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		category = url.strip().split('/')[-3]
		filename = "ajio_"+category+'.txt'

		if os.path.exists(filename)==False:
			UrlsList(url).list_of_products(filename)
		f = open(filename,'r')
		product_urls=f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		for i,url in enumerate(products):
			print(i+1,url)
			Ajio(url).product_data(folder_path)

		if len(os.listdir(folder_path)) == len(product_urls):
			return True
		else:
			return False

	elif 'flipkart' in url:
		from ..utils.flipkart import UrlsList
		product_urls = UrlsList(url).list_of_products()

		folder_path='flipkart_products'
		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		for url in product_urls:
			Flipkart(url).product_data(folder_path)

	elif 'limeroad' in url:
		from ..utils.limeroad import UrlsList
		product_urls = UrlsList(url).list_of_products()

		folder_path='limeroad_products'
		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		for url in product_urls:
			Limeroad(url).product_data(folder_path)

	else:
		raise ValueError("Enter a valid search URL from the following market places: Flipkart, Ajio, Bewakoof, Limeroad")
