import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import common_texts
import gensim.downloader as api
import time
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import tensorflow_hub as hub
from absl import logging


"""
###########################
# GLOVE EMBEDDINGS

embeddings_dict = {}
words_list=[]

start = time.time()
with open('DescriptionMatcher/services/glove.6B/glove.6B.50d.txt','r') as f:
	for line in f:
		values = line.split(' ')
		word = values[0] 
		words_list.append(word)
		coefs = np.asarray(values[1:], dtype='float32') 
		embeddings_dict[word] = coefs
	f.close()
end = time.time()
print('GloVe data loaded in',end-start,'seconds')

##########################
"""


"""
###########################
# WORDTOVEC EMBEDDINGS


start = time.time()
word2vec_model = KeyedVectors.load_word2vec_format('DescriptionMatcher/services/GoogleNews-vectors-negative300.bin',binary=True)
end = time.time()
print("Word2Vec model loaded in", end-start,'seconds')

##########################
"""


"""
##########################
# FASTTEXT EMBEDDINGS

fasttext_wordlist=[]
fasttext_embedding={}


start = time.time()
with open('DescriptionMatcher/services/wiki-news-300d-1M-subword.vec') as f:
	for line in f:
		values = line.split(' ')
		word = values[0]
		fasttext_wordlist.append(word)
		coefs = np.array(values[1:],dtype='float32')
		fasttext_embedding[word] = coefs
	f.close()
end = time.time()
print('FastText model loaded in ',end-start,' seconds')

##########################
"""


###########################
# SENTENCE BERT TRANSFORMER

start= time.time()
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
end=time.time()
print('Sbert model loaded in',end-start,'seconds')

###########################


"""
##########################
# UNIVERSAL SENTENCE ENCODER

start = time.time()
module = 'DescriptionMatcher/services/universal-sentence-encoder_4'
unse_model = hub.load(module)
logging.set_verbosity(logging.ERROR)
end = time.time()
print("Universal Sentence Encoder model was loaded in", end - start,"seconds.")

##########################
"""


##########################
# NEURAL NETWORK LANGUAGE MODEL (NNLM) model

start = time.time()
nnlm_model = hub.load('DescriptionMatcher/services/nnlm-en-dim50_2')
end = time.time()
print("NNLM model was loaded in", end - start,"seconds.")

##########################

