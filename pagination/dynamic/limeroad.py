import json
import requests
from lxml import html
import re
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


url='https://www.limeroad.com/t-shirts'
category = "Men's T-Shirts"

filename = 'limeroad_' + category + '.txt'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver  =webdriver.Firefox(options=options, executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(url)
driver.maximize_window()
total_count = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[1]/div/div/div").get_attribute('innerText')
total_count = int(re.sub(r'[^\d]','',total_count))

print("Total count", total_count)

urls_list=[]
i=1

count=0
flag = 0

while len(urls_list)<total_count:
	time.sleep(2)
	try:
		content = driver.find_element_by_css_selector('div.prdC:nth-child('+str(i)+') > a:nth-child(1)')	
		_url_ = content.get_attribute('href')
		print(_url_)
		urls_list.append(_url_)

		f = open(filename,'a+')
		f.write(_url_+'\n')
		f.close()

		count=0

	except NoSuchElementException:
		print("No URL")
		count+=1
	
	if i%6 == 0:
		content.send_keys(Keys.PAGE_DOWN)
		print("Scrolling down!")

	if count>10:
		content.send_keys(Keys.PAGE_UP)
		print("Scrolling up!")
		flag+=1
		count = 0

	if flag > 10:
		break

	i+=1
	print(len(urls_list))


if len(urls_list)== total_count:
	print("All URLs were successfully retreived!")

else:
	print("Some URLs are missing")

