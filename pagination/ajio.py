from selenium import webdriver
import time
import json
from selenium.common.exceptions import StaleElementReferenceException

url = 'https://www.ajio.com/men-tshirts/c/830216014'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options,executable_path='/home/likhitha/.firefox/geckodriver')

driver.get(url)
driver.maximize_window()

total_content = driver.find_elements_by_xpath('//script[@type="application/ld+json"]')[2].get_attribute('innerText')
total_items = int(json.loads(total_content)['numberOfItems'])

SCROLL_TIME=15
STEP=1000

start_length = 0
end_length = STEP

urls_list=[]

category = url.strip().split('/')[-3]


print(total_items)
print("********************************************************************")

print("Finding last height..")
last_height = driver.execute_script("return document.body.scrollHeight")

i=0
while True:
	driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
	time.sleep(5)

	new_height = driver.execute_script("return document.body.scrollHeight")

	if last_height ==new_height:
		i+=1
	if i>5:
		break
	last_height= new_height

	print(last_height)

print("The last height is {}".format(last_height))

print("Refreshing the page..")
driver.refresh()
time.sleep(10)
print("Done!")

prev_len =0 
curr_len=-1
j=0

while start_length < last_height:
	print("Scrolling to {}".format(end_length))
	driver.execute_script("window.scrollTo("+str(start_length)+","+str(end_length)+")")
	time.sleep(2)
	curr_len = driver.execute_script("return document.body.scrollHeight")
	start_length+=STEP
	end_length+=STEP

	if prev_len == curr_len:
		j+=1

	if j>2:
		driver.execute_script("window.scrollTo("+str(curr_len)+","+str(curr_len-3000)+")")
		print("Scrolling up!")
		time.sleep(5)
		j=0
	
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
		f = open('test2.txt','w')
		f.write(all_urls)
		f.close()

if len(urls_list)== total_items:
	print("All URLs were successfully retreived!")

else:
	print("Some URLs are missing")
