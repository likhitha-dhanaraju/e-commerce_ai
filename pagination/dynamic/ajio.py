import json
import requests
from lxml import html
import re
import os
import numpy as np
from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException

url = 'https://www.ajio.com/men-tshirts/c/830216014'
category = "Men's T-Shirts"

filename = 'ajio_'+ category + '.txt'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,
			executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(url)
driver.maximize_window()

total_content = driver.find_elements_by_xpath('//script[@type="application/ld+json"]')[2].get_attribute('innerText')
total_count = int(json.loads(total_content)['numberOfItems'])
print("total_count",total_count)


last_height = 1500000
print("The last height is {}".format(last_height))

urls_list=[]

STEP=2500
start_length = 0
end_length = STEP
prev_len =0 
curr_len=-1
j=0

f = open(filename,'a+')

while start_length< last_height:
	print("Scrolling to {}".format(end_length))
	driver.execute_script("window.scrollTo("+str(start_length)+","+str(end_length)+")")
	time.sleep(2)
	curr_len = driver.execute_script("return document.body.scrollHeight")
	start_length+=STEP
	end_length+=STEP

	if prev_len == curr_len:
		driver.execute_script("window.scrollTo("+str(curr_len)+","+str(curr_len-3000)+")")
		print("Scrolling up!")
		time.sleep(5)
			
	print("curr_len",curr_len)
	print("prev_len",prev_len)
	try:
		content = driver.find_elements_by_xpath("//div[@class='items']/div/div/div/a")
		
		for item in content:
			_url_ = item.get_attribute('href')
			urls_list.append(_url_)
	
		urls_list = list(set(urls_list))
		prev_len = curr_len

	except StaleElementReferenceException:
	
		print("StaleElementReferenceException here. Continuing..")

	print(len(urls_list))

	prev_len = curr_len

	if end_length%50000 == 0:

		all_urls=""
		for url in urls_list:
			all_urls+=url+'\n'

		f = open(filename,'w')
		f.write(all_urls)
		f.close()

if len(urls_list)== total_count:
	print("All URLs were successfully retreived!")

else:
	print("Some URLs are missing")

