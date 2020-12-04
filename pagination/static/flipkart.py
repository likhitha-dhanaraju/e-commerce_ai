from selenium import webdriver
import time
import json
import re

base_url = 'https://www.flipkart.com/clothing-and-accessories/topwear/tshirts/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy'
add_page='&page='

category = "Men's T-Shirts"
filename = 'flipkart_'+ category +'.txt'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,
			 executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(base_url)
driver.maximize_window()

number_of_pages = 26

print("Number of pages", number_of_pages - 1 )

urls_list=[]
SCROLL_TIME = 2


count=1

for page in range(1, number_of_pages ):
	print("Page number",page)
	url = base_url + add_page+str(page)
	driver.get(url)
	time.sleep(SCROLL_TIME)
	driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
	time.sleep(SCROLL_TIME)

	for num1 in range(2,12):
		xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div['+str(num1)+']'
			    
		for num2 in range(1,5):
			try:
				sub_xpath =xpath+ '/div/div['+str(num2)+']/div/a'
				content = driver.find_elements_by_xpath(sub_xpath)
				_url_ = content[0].get_attribute('href')
				print(count, _url_+'\n')
				urls_list.append(_url_)
				f=open(filename, 'a+')
				f.write(_url_+'\n')
				f.close()
				count+=1

			except IndexError:
				print("Skipping few items")


if len(urls_list)==total_count:
	print("All URLs are retreived")
else:
	print("Some URLs are missing")
