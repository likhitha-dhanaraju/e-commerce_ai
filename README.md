# pagination

Scrapping products from the search page to the following websites.

**Dynamic websites:**

1. Ajio
2. Bewakoof
3. Limeroad

**Static websites:**

1. Flipkart
2. Myntra

### Instructions to use

1. Clone the repository - `git clone https://bitbucket.org/vectorised/matching-tool.git`
2. cd `matching-tool/pagination/`
3. Install the required libraries - `pip install -r requirements.txt`
4. Enter the `URL` and `category` name in the file and run the program.


# description_matcher

Given two product urls, data and images are extracted. The similarity between the names and keywords of the products are shown using various embeddings with cosine similarity 

### Instructions to run:

1. Clone the repository. `git clone https://bitbucket.org/vectorised/matching-tool.git`

2. Move into the repository. `cd matching-tool/`

3. Move into the repository `cd description_matcher/`

4. Install the necessary packages. `pip install -r requirements.txt`

5. Download the required models, unzip them and place them in the **services** folder.
	i. **Universal Sentence Decoder**: `https://tfhub.dev/google/universal-sentence-encoder/4`
	ii. **GloVe vectors**: `http://nlp.stanford.edu/data/glove.6B.zip`
	iii. **Word2Vec model**: `https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit`
	iv. **Neural Network Language Model (NNLM)**: `https://tfhub.dev/google/nnlm-en-dim50/2`

6. Start the server. `python manage.py runserver`

7. Send API requests in Postman as follows: 

```python

METHOD: 'GET'
URL: 'https://server-url:port/matcher/'

PARAMS: 

Key: 'URL1'
Value: # full url of the product
	   # Ex. 'https://www.ajio.com/fig-round-neck-top-with-ribbed-hems/p/440993597_yellow'

Key: 'URL2'
Value: # full url of the second product
	   # Ex. https://www.ajio.com/pannkh--novelty-top-/p/461020470_blue

```

# products_scrapper

Given the search page of a website, all products are scraped and the data is stored in a JSON file along with the images extracted. 
The API first collates the list of products available on the search page exhaustively into a `.txt` file. It then reads each product url from the text file and extracts the product data.

Codes for the following websites are available:
1. Ajio 
2. Bewakoof
3. Flipkart ( can scrape only 25 pages. Each page has 40 products. So a maximum of 1000 products can be scraped from each search page )
4. Limeroad
5. Myntra ( scraping is very slow )

### Instructions to run:

1. Clone the repository. `git clone https://bitbucket.org/vectorised/matching-tool.git`

2. Move into the repository. `cd matching-tool/`

3. Move into the repository. `cd products_scrapper/`

4. Install the necessary packages. `pip install -r requirements.txt`

5. Start the server. `python manage.py runserver`

6. Send API requests in Postman as follows: 

```python

METHOD: 'GET'

URL: 'https://server-url:port/list/'

PARAMS:

Key: 'URL'
Value: # full url of the product
	   # Ex. 'https://www.ajio.com/women-tops/c/830316017'

Key: 'Folder'
Value: # Category name of the products
	   # Ex. Women's Tops

```

# image_captioning_app
 
Given the image of a product, a suitable product name is generated.

### Instructions to run:

1. Clone the repository. `git clone https://bitbucket.org/vectorised/matching-tool.git`

2. Move into the repository. `cd matching-tool/`

3. Move into the repository. `cd image_captioning_app/`

4. Install the necessary packages. `pip install -r requirements.txt`

5. Download the trained model files from [here](https://drive.google.com/drive/folders/121OfXaiBI89Mv4cIDRr67hYiU5STwUeZ?usp=sharing) and place it in the `model` folder.

6. Start the server. `python manage.py runserver`

7. Send API requests in Postman as follows: 

```python

METHOD: 'POST'

URL: 'https://server-url:port/caption/'

BODY -> form-data

'When you hover over Key, you can select "File" from the dropdown menu'

Key: 'image'
Value: # upload the file here

Key: 'model_name'
Value: #name of the saved file name

Key: 'mapping_filename'
Value: #name of the json file containing data for prediction purposed.

```
*Cuurently, the API has been written for ImageCaptioning_V4*

# scrappers

Scrapping product details from the following websites - Ajio, Bewakoof, Flipkart, Limeroad and Myntra.

### Instructions to use

1. Clone the repository - `git clone https://bitbucket.org/vectorised/matching-tool.git`
2. cd `matching-tool/scrappers/`
3. Install the required libraries - `pip install -r requirements.txt`
4. Enter the `URL` of the product in the file and run the program.

# imageCaptioning

Directory containing the different versions of notebooks and python scripts to train the image captioning notebook.

### Instructions to run

1. Clone the repository - `git clone https://bitbucket.org/vectorised/matching-tool.git`
2. cd `matching-tool/imageCaptioning/`
3. To run the notebooks, go to the sppecific version and run the notebook.
4. To run the python scripts, go to the directory `Python Scripts`. Refer to the script for the arguments to be provided.
