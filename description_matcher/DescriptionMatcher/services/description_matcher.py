import os
import sys
from ..utils.market_place_finder import MRFinder
from scipy.spatial.distance import cosine
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from keras.preprocessing.sequence import pad_sequences
import tensorflow_hub as hub
import tensorflow as tf


# GLOVE EMBEDDINGS. Uncomment the below line.
#from ..settings import embeddings_dict, words_list


# FASTTEXT EMBEDDINGS. Uncomment the below line.
#from ..settings import fasttext_wordlist,fasttext_embedding

# WORD2VEC EMBEDDINGS. Uncomment the below line.
#from ..settings import word2vec_model

# SENTENCE BERT TRANSFORMER. Uncomment the below line.
from ..settings import sbert_model

# UNIVERSAL SENTENCE ENCODER. Uncomment the below line.
#from ..settings import unse_model

# LASER (Language-Agnostic SEntence Representations) model. Uncomment the below line.
from laserembeddings import Laser 

# NNLM ( Neural Network Language Model ). Uncomment the below line.
from ..settings import nnlm_model


class Descriptor():
	def __init__(self,url1,url2):
		self.url1 = url1
		self.url2 = url2
		self.productdata1 = MRFinder(self.url1).choosing()
		self.productdata2 = MRFinder(self.url2).choosing()

		self.keywords1 , self.keywords2= self.productdata1['keywords'],self.productdata2['keywords']
		self.name1,self.name2 = self.productdata1['product_name'], self.productdata2['product_name']

	####  BAG OF WORDS  ####

	def bag_of_words(self,text_list,words_to_index,length):
		result_vector = np.zeros(length)
		for word in text_list:
			if word in words_to_index:
				result_vector[words_to_index[word]]+=1
		return result_vector

	def cosine(self,vec1,vec2):
		num = float(np.dot(vec1.transpose(),vec2))
		denom = float(np.dot(np.sqrt(np.sum(vec1**2)),np.sqrt(np.sum(vec2**2))) + 1e-5)
		return float(num / denom)	

	def bow_similarity_quotient(self):

		words = sorted(list(set(self.keywords1+self.keywords2)))
		values = range(len(words))
		words_to_index = {words[i]:values[i] for i in range(len(words))}
		
		#### KETWORDS SIMILARITY

		keyvector1= self.bag_of_words(self.keywords1,words_to_index,len(words_to_index)).reshape(-1,1)
		keyvector2 = self.bag_of_words(self.keywords2,words_to_index,len(words_to_index)).reshape(-1,1)

		keyword_similarity = self.cosine(keyvector1,keyvector2)

		#### NAME SIMILARITY
		
		words = sorted(list(set(self.name1+self.name2)))
		values = range(len(words))
		words_to_index = {words[i]:values[i] for i in range(len(words))}

		namevector1 = self.bag_of_words(self.name1,words_to_index,len(words_to_index)).reshape(-1,1)
		namevector2 = self.bag_of_words(self.name2,words_to_index,len(words_to_index)).reshape(-1,1)

		name_similarity = self.cosine(namevector1,namevector2)

		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keyword_similarity,4),
				'overall_similarity':round(float(+(0.1*name_similarity)+(0.9*keyword_similarity)),4)
				}

	#### HASH SIMILARITY ####

	def custom_cosine(self,vec1,vec2):
		similarity=[]
		for i in vec1:
			temp=[]
			for j in vec2:
				temp.append(self.cosine(i.reshape(-1,1),j.reshape(-1,1)))
			similarity.append(max(temp))
		return sum(similarity)/len(similarity)

	def hash_similarity_quotient(self):
		## HASH VECTORIZER

		n_features = 10
		vectorizer = HashingVectorizer(n_features=n_features)

		#### KEYWORD SIMILARITY

		keyvector1 = vectorizer.transform(list(set(self.keywords1))).toarray()
		keyvector2 = vectorizer.transform(list(set(self.keywords2))).toarray()
		keywords_similarity = self.custom_cosine(keyvector1,keyvector2)

		#### NAME SIMILARITY

		namevector1 = vectorizer.transform(self.name1).toarray()
		namevector2 = vectorizer.transform(self.name2).toarray()
		name_similarity = self.custom_cosine(namevector1, namevector2)
	
		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4)
				}


	#### TF-IDF SIMILARITY ####

	def tf_idf_vectoriser(self,wordlist):

		vector = self.tfidf.transform(wordlist).toarray()
		return np.array(vector)

	def tf_idf_similarity_quotient(self):

		self.tfidf = TfidfVectorizer(analyzer='word',max_features=100).fit(self.keywords1+self.keywords2)

		#### KEYWORDS SIMILARITY
		keyvector1 = self.tf_idf_vectoriser(self.keywords1)
		keyvector2 = self.tf_idf_vectoriser(self.keywords2)

		keywords_similarity = self.custom_cosine(keyvector1,keyvector2)

		#### NAME SIMILARITY
		name1 = self.tf_idf_vectoriser(self.name1)
		name2 = self.tf_idf_vectoriser(self.name2)
		name_similarity = self.custom_cosine(name1,name2)

		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4)
				}

	#### GLOVE SIMILARITY ####

	def custom_embeddings_cosine(self,wordlist1, wordlist2, embedding_dict):
		answer=[]
		number = len(wordlist1)
		for word1 in wordlist1:
			temp=[]
			for word2 in wordlist2:
				if (word1 in words_list) and (word2 in words_list):
					temp.append(self.cosine(embedding_dict[word1],embedding_dict[word2]))
			if temp!=[]:
				answer.append(sum(temp)/len(wordlist2))
		return sum(answer)/int(number)

	def average_cosine_similarity(self,vec1,vec2):
		max_len = max(vec1.shape[0],vec2.shape[0])
		
		vec1_avg = np.average(vec1,axis=1)
		vec2_avg = np.average(vec2,axis=1)

		padded_sequences = pad_sequences([vec1_avg,vec2_avg],maxlen= max_len,dtype='float32')
		return self.cosine(padded_sequences[0],padded_sequences[1])

	def glove_encoding(self,wordlist):
		vector =[]
		for i in wordlist:
			if i in words_list:
				vector.append(embeddings_dict[i])
		return np.array(vector)

	def glove_similarity_quotient(self):
		#### KEYWORD SIMILARITY

		keyvector1, keyvector2  = self.glove_encoding(sorted(list(set(self.keywords1)))),self.glove_encoding(sorted(list(set(self.keywords2))))
		keywords_similarity = self.custom_embeddings_cosine(self.keywords1,self.keywords2, embeddings_dict)
		average_keyword_similarity = self.average_cosine_similarity(keyvector1,keyvector2)

		#### NAME SIMILARITY

		namevector1, namevector2 = self.glove_encoding(self.name1), self.glove_encoding(self.name2)
		name_similarity = self.custom_embeddings_cosine(self.name1,self.name2,embeddings_dict)
		average_name_similarity = self.average_cosine_similarity(namevector1,namevector2)

		return {
				#'name_similarity':round(name_similarity,4),
				#'keywords_similarity':round(keywords_similarity,4),
				#'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4),
				'name_similarity':round(average_name_similarity,4),
				'keyword_similarity':round(average_keyword_similarity,4),
				'overall_similarity':round(float((0.1*average_name_similarity)+(0.9*average_keyword_similarity)),4),
				}
				
	#### WORD_TO_VEC SIMILARITY ####

	def word2vec_encoding(self,wordlist):
		vector =[]
		for i in wordlist:
			if i in self.word2vec:
				vector.append(self.word2vec[i])
		return np.array(vector)

	def word2vec_cosine(self,wordlist1, wordlist2):
		answer=[]
		for word1 in wordlist1:
			temp=[]
			for word2 in wordlist2:
				if word1 in self.word2vec and word2 in self.word2vec:
					temp.append(self.word2vec.similarity(word1,word2))
			#answer.append(max(temp))
			answer.append(np.average(temp))
		return np.average(answer)

	def word2vec_similarity_quotient(self):
		#self.word2vec = Word2Vec(sorted([self.keywords1+self.keywords2+self.name1+self.name2]), size=10, window =5,min_count=1, workers=-1)
		self.word2vec = word2vec_model

		#### KEYWORD SIMILARITY
		keywords_similarity =self.word2vec_cosine(self.keywords1,self.keywords2)
		keyvector1, keyvector2 = self.word2vec_encoding(self.keywords1),self.word2vec_encoding(self.keywords2)
		#print(self.word2vec.wmdistance(keyvector1,keyvector2))
		average_name_similarity =self.average_cosine_similarity(keyvector1,keyvector2)

		#### NAME SIMILARITY
		
		name_similarity = self.word2vec_cosine(self.name1,self.name2)
		namevector1, namevector2 = self.word2vec_encoding(self.name1),self.word2vec_encoding(self.name2)
		average_keyword_similarity = self.average_cosine_similarity(namevector1, namevector2)
	
		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4),
				'average_name_similarity': round(average_name_similarity,4),
				'average_keywords_similarity': round(average_keyword_similarity,4)
				}

	#### FASTEXT ENCODING SIMILARITY 

	def fasttext_encoding(self,wordlist):
		vector =[]
		for i in wordlist:
			if i in words_list:
				vector.append(fasttext_embedding[i])
		return np.array(vector)

	def fasttext_similarity_quotient(self):
		
		#### KEYWORDS SIMILARITY

		keyvector1, keyvector2  = self.fastetx_encoding(sorted(list(set(self.keywords1)))),self.fasttext_encoding(sorted(list(set(self.keywords2))))
		keywords_similarity = self.custom_embeddings_cosine(self.keywords1,self.keywords2,fasttext_embedding)
		average_keyword_similarity = self.average_cosine_similarity(keyvector1,keyvector2)

		#### NAME SIMILARITY

		namevector1, namevector2 = self.fasttext_encoding(self.name1), self.fasttext_encoding(self.name2)
		name_similarity = self.custom_embeddings_cosine(self.name1,self.name2,fasttext_embedding)
		average_name_similarity = self.average_cosine_similarity(namevector1,namevector2)

		return {
				#'name_similarity':round(name_similarity,4),
				#'keywords_similarity':round(keywords_similarity,4),
				#'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4),
				'name_similarity':round(average_name_similarity,4),
				'keyword_similarity':round(average_keyword_similarity,4),
				'overall_similarity':round(float((0.1*average_name_similarity)+(0.9*average_keyword_similarity)),4),
				}


	#### UNIVERSAL SENTENCE ENCODING SIMILARITY

	def unse_cosine(self,wordlist1,wordlist2):
		answer=[]
		for word1 in wordlist1:
			temp=[]
			for word2 in wordlist2:
				padded = pad_sequences([word1,word2],dtype='float32')
				temp.append(self.cosine(padded[0],padded[1]))
			answer.append(sum(temp)/len(wordlist2))

		return sum(answer)/len(wordlist1)
	

	def unse_similarity_quotient(self):

		self.unse_model = unse_model

		keyvector1 = np.array(self.unse_model(self.keywords1))
		keyvector2 = np.array(self.unse_model(self.keywords2))

		average_keyword_similarity = self.average_cosine_similarity(keyvector1,keyvector2)
		keywords_similarity = self.unse_cosine(keyvector1,keyvector2)

		namevector1 = np.array(self.unse_model(self.name1))
		namevector2 = np.array(self.unse_model(self.name2))

		average_name_similarity = self.average_cosine_similarity(namevector1,namevector2)
		name_similarity = self.unse_cosine(namevector1,namevector2)

		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4),
				'average_name_similarity': round(average_name_similarity,4),
				'average_keywords_similarity': round(average_keyword_similarity,4),
				}

	#### NNLM ENCODING
	
	def nnlm_encoding(self,wordlist):
		embed = hub.load('DescriptionMatcher/services/nnlm-en-dim50_2')
		vector = embed(wordlist)
		max_len = vector.shape[1]

		answer=[]
		for i in range(max_len):
			answer.append(np.array(vector[:,i]))

		return np.array(answer)

	def nnlm_similarity_quotient(self):

		keyvector1 = self.nnlm_encoding(self.keywords1)
		keyvector2 = self.nnlm_encoding(self.keywords2)

		average_keywords_similarity = self.average_cosine_similarity(keyvector1,keyvector2)
	
		namevector1 = self.nnlm_encoding(self.name1)
		namevector2 = self.nnlm_encoding(self.name2)

		average_name_similarity = self.average_cosine_similarity(namevector1,namevector2)
	
		return {
				'name_similarity':round(average_name_similarity,4),
				'keywords_similarity':round(average_keywords_similarity,4),
				'overall_similarity':round(float((0.1*average_name_similarity)+(0.9*average_keywords_similarity)),4)
				}	
	## Sentence similarity
	
	#### LASER EMBEDDINGS

	def laser_similarity_quotient(self):
	
		laser = Laser()

		keywords1 = " ".join(self.keywords1)
		keywords2 = " ".join(self.keywords2)

		keywords_embeddings = laser.embed_sentences([keywords1,keywords2],lang='en')
		keywords_similarity = self.cosine(keywords_embeddings[0],keywords_embeddings[1])

		name1 = " ".join(self.name1)
		name2 = " ".join(self.name2)

		name_embeddings = laser.embed_sentences([name1,name2],lang='en')
		name_similarity = self.cosine(name_embeddings[0],name_embeddings[1])

		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4)
				}	

	#### SBERT EMBEDDINGS

	def sbert_similarity_quotient(self):

		#### KEYWORDS SIMILARITY
		keywords1 = " ".join(self.keywords1)
		keywords2 = " ".join(self.keywords2)

		keywords_embeddings = sbert_model.encode([keywords1,keywords2])
		keywords_similarity = self.cosine(keywords_embeddings[0],keywords_embeddings[1])


		#### NAME SIMILARITY
		name1 = " ".join(self.name1)
		name2 = " ".join(self.name2)

		name_embeddings = sbert_model.encode([name1,name2])
		name_similarity = self.cosine(name_embeddings[0],name_embeddings[1])

		return {
				'name_similarity':round(name_similarity,4),
				'keywords_similarity':round(keywords_similarity,4),
				'overall_similarity':round(float((0.1*name_similarity)+(0.9*keywords_similarity)),4)
				}	

#https://medium.com/@adriensieg/text-similarities-da019229c894
 