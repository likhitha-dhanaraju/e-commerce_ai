from selenium import webdriver
import time
import json
import re

url = 'https://www.bewakoof.com/men-t-shirts'
category = "Men's T-Shirts"

filename = 'bewakoof_' + category + '.txt'
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,
		executable_path='/home/likhitha/.firefox/geckodriver')
driver.get(url)
driver.maximize_window()

total_content = driver.find_element_by_css_selector('.headingInner > span:nth-child(2)')
total_count = total_content.get_attribute('innerText')
total_count = int(re.sub(r'[^\d]','',total_count))
print("Total_count",total_count)

SCROLL_TIME=2
STEP=2500
start_length = 0
end_length = STEP
i=0

urls_list=[]

	
f= open(filename,'a+')

while i< total_count:
	driver.execute_script("window.scrollTo("+str(start_length)+","+str(end_length)+")")
	time.sleep(SCROLL_TIME)

	start_length+=STEP
	end_length+=STEP

	id_name ='testProductcard_'+str(i+1)
	content = driver.find_element_by_id(id_name).find_element_by_xpath('a')
	i+=1
	_url_= content.get_attribute('href')
	print(i, _url_)
	urls_list.append(_url_)
	f.write(_url_+'\n')

f.close()

print(len(list(set(urls_list))))

if len(urls_list) == total_count:
	print("All URLs are extracted.")

else:
	print("Some URLs are missing.")