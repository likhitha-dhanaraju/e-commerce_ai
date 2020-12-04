import json
from lxml import html
import re
from selenium import webdriver
import time

url = 'https://www.myntra.com/women-jeans-jeggings'
category = "Wonen's Jeans"

sub_url = '?p='
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,
			executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(url)
driver.maximize_window()

total_count = driver.find_element_by_css_selector('.title-count').get_attribute('innerText')
total_count = int(re.sub(r'[^\d]','',total_count))
print(total_count)

num_pages = int(total_count/50)+2
print(num_pages)

SCROLL_TIME = 5
count=1

urls_list=[]

filename = 'myntra_' + category + '.txt'

f = open(filename,'w')

for num1 in range(1,num_pages):
	driver.get(url+sub_url+str(num1))
	driver.execute_script('window.scrollTo(0,5000)')
	time.sleep(SCROLL_TIME)

	for num2 in range(1,51):
		_url_ = driver.find_element_by_css_selector(
			'li.product-base:nth-child('+str(num2)+') > a:nth-child(2)').get_attribute('href')
		print(count, _url_)
		count+=1
		urls_list.append(_url_)
		f.write(_url_+'\n')

f.close()
if len(urls_list) == total_count:
	print("All URLs are retrieved")
else:
	print("Some URLs are missing")
