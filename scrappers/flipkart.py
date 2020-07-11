from selenium import webdriver
import time
import json
import re

base_url = 'https://www.flipkart.com/clothing-and-accessories/topwear/tshirts/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy'
add_page='&page='


options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,executable_path='/home/likhitha/.firefox/geckodriver')

driver.get(url)
driver.maximize_window()

total_count = driver.find_element_by_css_selector('.eGD5BM').get_attribute('innerText')
total_count = int(total_count.strip().split(' ')[-2])

number_of_pages = int(total_count/40)

SCROLL_TIME = 15
urls_list=[]
for page in range(1,number_of_pages+1):
	url = base_url+add_page+str(page)
	driver.get(url)
	driver.execute_script('window.scrollTo(0,document.window.scrollHeight)')
	time.sleep(SCROLL_TIME)

	for num1 in rnage(2,11):
		xpath = '/html/body/div/div/div[3]/div[2]/div[1]/div[2]/div['+str(num1)+']/div'
		content = driver.find_elements_by_xpath(xpath)

		print(len(content))
		for item in content:
			element = item.find_element_by_xpath('/div/a')
			_url_ = element.get_attribute('href')
			urls_list.append(_url_)

if len(urls_list)==total_count:
	print("All URLs are retrieved")
else:
	print("Some URLs are missing")

with open("flipkart.txt",'w') as f:
	f.write(urls_list)
	f.close()
