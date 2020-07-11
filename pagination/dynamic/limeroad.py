from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import json
import re

url='https://www.limeroad.com/t-shirts'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(url)
driver.maximize_window()

product_ids = ["prdC bgF br4 fs12 fg2t dIb vT pR taC bs bd2E   m6",
 "bs oH strC pR taC bd2E br4 bgF m6  fg2t dIb vT"]

total_count = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[1]/div/div/div").get_attribute('innerText')
total_count = int(re.sub(r'[^\d]','',total_count))

urls_list=[]
i=1

len_content = len(urls_list)

search_item = url.strip().split('/')[-1]

with open("limeroad_"+search_item+'.txt','a+') as f:
	while len(urls_list)<total_count:
		time.sleep(2)
		try:
			content = driver.find_element_by_css_selector('div.prdC:nth-child('+str(i)+') > a:nth-child(1)')
			_url_ = content.get_attribute('href')
			print(_url_)
			content.send_keys(Keys.PAGE_DOWN)
			urls_list.append(_url_)
			f.write(_url_+'\n')
			
		except NoSuchElementException:
			print("No URL")

		i+=1

print(len(list(set(urls_list))))

if len(urls_list)==total_count:
	print("All URLs are extracted.")
else:
	print("Some URLs are missing.")

with open("flipkart.txt",'w') as f:
	f.write(urls_list)