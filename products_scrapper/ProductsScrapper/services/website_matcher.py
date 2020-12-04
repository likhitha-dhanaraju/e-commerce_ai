import os
import json
import re
from selenium.common.exceptions import TimeoutException

def WebsiteMatcher(url, folder):

	if 'bewakoof' in url:
		from ..utils.bewakoof import UrlsList, Bewakoof
	
		folder_path='bewakoof_products/'+folder

		if os.path.exists('bewakoof_products')==False:
			os.mkdir('bewakoof_products')

		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		if not os.path.exists('products_list'):
			os.mkdir('products_list')

		filename = "products_list/bewakoof_"+folder+'.txt'

		if not os.path.exists(filename):
			UrlsList(url).list_of_products(filename)

		f= open(filename,'r')
		product_urls = f.readlines()
		f.close()
		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		print("Number of products in file", len(products))

		for i,url in enumerate(products):

			folder_name = url.strip().split('/')[-1]
			folder_name = re.sub('/','',folder_name)
			parent_folder = os.path.join(folder_path,'bewakoof_'+folder_name)

			if not os.path.exists(parent_folder):
				try:
					Bewakoof(url).product_data(folder_path)
				except (json.JSONDecodeError, IndexError, TimeoutException) as e:
					print("Skipping this ",e)

		if len(os.listdir(folder_path)) == len(product_urls):
			return True
		else:
			return False

	elif 'ajio' in url:
		from ..utils.ajio import UrlsList, Ajio
		
		folder_path='ajio_products/'+folder

		if os.path.exists('ajio_products')==False:
			os.mkdir('ajio_products')

		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		if not os.path.exists('products_list'):
			os.mkdir('products_list')

		filename = "products_list/ajio_"+folder+'.txt'

		if os.path.exists(filename)==False:
			UrlsList(url).list_of_products(filename)
		f = open(filename,'r')
		product_urls=f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		print("Number of products in file", len(products))
		
		for i,url in enumerate(products):
			print(i+1,url)
			folder_name = url.strip().split('/')[-1]
			parent_folder = os.path.join(folder_path,'ajio_'+folder_name)

			if not os.path.exists(parent_folder):
				try:
					Ajio(url).product_data(folder_path)
					
				except (json.JSONDecodeError, IndexError, TimeoutException) as e:
					print("Skipping this ",e)

		if len(os.listdir(folder_path)) == len(product_urls):
			return True
		else:
			return False

	elif 'flipkart' in url:
		from ..utils.flipkart import UrlsList, Flipkart

		folder_path='flipkart_products/'+folder
		if os.path.exists('flipkart_products')==False:
			os.mkdir('flipkart_products')

		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		if not os.path.exists('products_list'):
			os.mkdir('products_list')

		filename = "products_list/flipkart_"+folder+'.txt'

		if os.path.exists(filename)==False:
			UrlsList(url).list_of_products(filename)
		
		f = open(filename,'r')
		product_urls = f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		print("Number of products in file", len(products))

		for i,url in enumerate(products):
			print(i+1,url)
			Flipkart(url).product_data(folder_path)

		if len(os.listdir(folder_path)) == len(products):
			return True
		else:
			return False

	elif 'limeroad' in url:
		from ..utils.limeroad import UrlsList, Limeroad

		if os.path.exists('limeroad_products')==False:
			os.mkdir('limeroad_products')

		folder_path='limeroad_products/'+folder

		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		if not os.path.exists('products_list'):
			os.mkdir('products_list')

		filename = "products_list/limeroad_"+folder+'.txt'

		if os.path.exists(filename)==False:
			UrlsList(url).list_of_products(filename)

		f = open(filename,'r')
		product_urls = f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		print("Number of products in file", len(products))

		for i,url in enumerate(products):
			print(i+1,url)
			folder_name = url.strip().split('?')[0].strip().split('/')[-1]
			parent_folder = os.path.join(folder_path,'limeroad_'+folder_name)

			if not os.path.exists(parent_folder):
				try:
					Limeroad(url).product_data(folder_path)
				except (json.JSONDecodeError, IndexError) as e:
					print("Skipping this.",e)

		if len(os.listdir(folder_path)) == len(products):
			return True
		else:
			return False

	elif 'myntra' in url:
		from ..utils.myntra import UrlsList, Myntra

		if os.path.exists('myntra_products')==False:
			os.mkdir('myntra_products')

		folder_path = 'myntra_products/'+folder

		if os.path.exists(folder_path)==False:
			os.mkdir(folder_path)

		if not os.path.exists('products_list'):
			os.mkdir('products_list')

		filename = 'products_list/myntra_'+folder+'.txt'

		if os.path.exists(filename)==False:
			UrlsList(url).list_of_products(filename)

		f = open(filename,'r')
		product_urls = f.readlines()
		f.close()

		products=[]
		for i in product_urls:
			products.append(i.strip().split('\n')[0])

		print("Number of products in file", len(products))
		
		for i,url in enumerate(products):
			print(i+1, url)
			folder_name = url.strip().split('/')[-3]+'_'+ url.strip().split('/')[-2]
			parent_folder = os.path.join(folder_path, 'myntra_'+ folder_name)

			if not os.path.exists(parent_folder):
				try:
					Myntra(url).product_data(folder_path)
				except (json.JSONDecodeError, IndexError, TimeoutException) as e:
					print("Skipping this ",e)

		if len(os.listdir(folder_path)) == len(products):
			return True
		else:
			return False

	else:
		raise ValueError("Enter a valid search URL from the following market places: Flipkart, Ajio, Bewakoof, Limeroad")