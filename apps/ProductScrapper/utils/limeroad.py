

class Limeroad():
	def __init__(self,url):
		self.url = url 
		r = requests.get(self.url).text
		parser = html.fromstring(r)
		strjson = parser.xpath('//script[@type="application/ld+json"]/text()')
		self.jobj = json.loads(strjson[0])

	def cleaning_data(self,wordlist):
		final_keywords=[]
		for wordd in wordlist:
			for word in wordd.strip().split(' '):
				word_ = re.sub(r'\d',' ', word)
				word_ = re.sub(r'[^\w]', ' ', word_)
				word_ = word_.strip().split(' ')
				for i in word_:
					if i!='':
						final_keywords.append(i)
		return final_keywords

	def product_data(self):
		
		productname = self.jobj['name'].lower().strip().split(' ')
		description = self.jobj['description'].lower()
		words = [word for word in description.strip().split(' ') if any(char not in SYMBOLS for char in word)]
		description_words = self.cleaning_data(words)
		price = self.jobj['offers']['price']
		availability =  self.jobj['offers']['availability'].split('/')[-1]
		condition = jobj['offers']['itemCondition'].split('/')[-1]
		marketplace = jobj_1['offers']['seller']['name'].split(' ')[0]

		image_urls=[]
		for img in jobj['image']:
			if img not in image_urls:
				image_urls.append(img)
		data= {
			'product_name':productname,
			'keywords':description_words,
			'image_urls':image_urls,
			'pricing':pricing,
			'condition':condition,
			'availability':availability
				}	
		filename = 'Limeroad_'+productname

		with open(filename+'.json','w') as file:
			json.dump(data,file)
			file.close()

		for val,image_url in enumerate(len(image_urls)):
			with open(filename+'_'+'image_'+str(val)+'_'+'.jpg','wb') as image:
				img_r = requests.get(image_url,stream=True)
				for block in img_r.iter_content(1024):
					if not block:
						break
					image.write(block)