from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Add, Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Concatenate, Flatten
from tensorflow.keras.layers import LSTM, Bidirectional, GRU
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50V2, VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras import backend as K
from tensorflow.keras import initializers, regularizers, constraints
from tensorflow.keras.layers import Layer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import GlobalAveragePooling2D, Reshape, TimeDistributed
from tensorflow.keras.callbacks import ReduceLROnPlateau
import numpy as np

def data_generator(descriptions, categories, photos, wordtoix, max_length, num_photos_per_batch):

	X1, X2, y1, y2 = list(), list(), list(), list()
	n=0
	# loop for ever over images
	while 1:
		for key, desc in descriptions.items():
			n+=1
			# retrieve the photo feature
			temp=main_dir
			try:
				photo = photos[key]
			
				for abc in range(1):
						# encode the sequence
				
					seq = [wordtoix[word] for word in desc.split(' ') if word in wordtoix]
						
					# split one sequence into multiple X, y pairs
					for i in range(1, len(seq)):
						# split into input and output pair
						in_seq, out_seq = seq[:i], seq[i]
						# pad input sequence
						in_seq = pad_sequences([in_seq], maxlen=max_length, dtype='float64')[0]
						# encode output sequence
						out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
						# store
					
						X1.append(photo)
						X2.append(in_seq)
						y1.append(out_seq)
						y2.append(categories[key])
			except KeyError:
				continue

			# yield the batch data
			if n==num_photos_per_batch:
				yield ([np.array(X1, dtype='float64'),
							np.array(X2, dtype='float64')], {'decoder_output':np.array(y1, dtype='float64'),
															'classifier_output':np.array(y2, dtype='float64')})
				
				X1, X2, y1, y2 = list(), list(), list(), list()
				n=0

class Attention(Layer):
	def __init__(self, step_dim,
				 W_regularizer=None, b_regularizer=None,
				 W_constraint=None, b_constraint=None,
				 bias=True, **kwargs):
 
		self.supports_masking = True
		self.init = initializers.get('glorot_uniform')

		self.W_regularizer = regularizers.get(W_regularizer)
		self.b_regularizer = regularizers.get(b_regularizer)

		self.W_constraint = constraints.get(W_constraint)
		self.b_constraint = constraints.get(b_constraint)

		self.bias = bias
		self.step_dim = step_dim
		self.features_dim = 0
		super(Attention, self).__init__(**kwargs)

	def get_config(self):
		config = super().get_config().copy()
		config.update({
				#'supports_masking':self.supports_masking,
				#'init':self.init,
				'W_regularizer': self.W_regularizer,
				'b_regularizer': self.b_regularizer,
				'W_constraint': self.W_constraint,
				'b_constraint': self.b_constraint,
				'bias': self.bias,
				'step_dim':self.step_dim,
				#'features_dim':self.features_dim,
		})
		return config

	def build(self, input_shape):
		assert len(input_shape) == 3

		self.W = self.add_weight(shape=(input_shape[-1],),
								 initializer=self.init,
								 name='{}_W'.format(self.name),
								 regularizer=self.W_regularizer,
								 constraint=self.W_constraint)
		self.features_dim = input_shape[-1]

		if self.bias:
			self.b = self.add_weight(shape=(input_shape[1],),
									 initializer='zero',
									 name='{}_b'.format(self.name),
									 regularizer=self.b_regularizer,
									 constraint=self.b_constraint)
		else:
			self.b = None

		self.built = True

	def compute_mask(self, input, input_mask=None):
		return None

	def call(self, x, mask=None):

		features_dim = self.features_dim
		step_dim = self.step_dim

		eij = K.reshape(K.dot(K.reshape(x, (-1, features_dim)), K.reshape(self.W, (features_dim, 1))), (-1, step_dim))

		if self.bias:
			eij += self.b

		eij = K.tanh(eij)
		a = K.exp(eij)
		a /= K.cast(K.sum(a, axis=1, keepdims=True) + K.epsilon(), K.floatx())

		a = K.expand_dims(a)
		weighted_input = x * a
		return K.sum(weighted_input, axis=1)

	def compute_output_shape(self, input_shape):
		return input_shape[0],  self.features_dim


## WITH CATEGORIES

### LOADING ANNOTATIONS FILE AND PREPROCESSING IT.
def load_doc(filename):
	file = open(filename, 'r')
	text = file.read()
	file.close()
	return text

# extract descriptions for images
def load_descriptions(doc):
	mapping = dict()
	cat_mapping = dict()
	for line in doc.split('\n'):
		tokens = line.strip().split('\t')
		if len(line) < 2:
			continue
		image_id, image_desc, image_cat = tokens[0], tokens[1], tokens[2]
		image_id = image_id.split('.')[0]
		image_desc = image_desc
		if image_id not in mapping:
			mapping[image_id] = image_desc
			cat_mapping[image_id] = image_cat
	return mapping, cat_mapping

def clean_descriptions(descriptions):
	table = str.maketrans('', '', string.punctuation)
	for key, desc in descriptions.items():
		desc = desc.split(' ')
		desc = [word.lower() for word in desc]
		desc = [w.translate(table) for w in desc]
		desc = [word for word in desc if len(word)>1]
		descriptions[key] =  ' '.join(desc)

### PREPROCESSING CAPTIONS FOR TRAINING
def load_captions(descriptions,train_product_ids):
	train_captions=[]
	for image_id in descriptions.keys():
		if image_id in train_product_ids:
			train_captions.append('startseq '+descriptions[image_id]+' endseq')
	
	return train_captions

## MAX LENGTH OF CAPTIONS

def max_len_caption(all_train_captions):   
	max_len = 0
	for caption in all_train_captions:
		max_len = max(max_len,len(caption.split()))
	print('Maximum length of caption= ',max_len)
	return max_len


def load_img_features(product_ids, image_dir):
	features=dict()
	product_ids_new = []
	in_layer = Input(shape=(224, 224, 3))
	model = VGG16(include_top=False, input_tensor=in_layer)

	image_dir = image_dir
	
	for j,id in enumerate(product_ids): 
		if j%100 == 0:
			print(j)
		try:
			image_name = image_dir+id+'.jpg'
			image=  load_img(image_name,target_size=(224, 224,3))
			image = img_to_array(image)
			image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
			image = preprocess_input(image)
			feature = model.predict(image, verbose=0)
			product_ids_new.append(id)
			features[id] = feature.reshape(7,7,512)
		except OSError:
		  print("Error with file")
  
	print("Loaded", len(features.keys()) ,"number of features" )

	return features, product_ids_new


def load_captions_dict(descriptions,train_product_ids):
	train_captions=dict()
	for image_id in descriptions.keys():
		if image_id in train_product_ids:
			train_captions[image_id]= 'startseq '+descriptions[image_id]+' endseq'
	
	return train_captions

def oneHotEncoding(x):
	ans = np.zeros((13))
	ans[x] = 1
	return ans

def load_categories_dict(categories, train_product_ids):
	train_categories=dict()
	for image_id in categories.keys():
		if image_id in train_product_ids:
			x = mapping_index.get_loc(categories[image_id])
			train_categories[image_id] = oneHotEncoding(x)
	return train_categories

def model_def(max_length_caption, vocab_size):

	ImageInput =Input(shape=(7,7,512,))
	ImageEncoder = Conv2D(512,(3,3),padding='same',activation='relu')(ImageEncoder)
	ImageEncoder = MaxPooling2D((2,2))(ImageEncoder)
	ImageEncoder = Conv2D(512,(1,1),padding='same',activation='relu')(ImageEncoder)
	ImageEncoder = Flatten()(ImageEncoder)
	ImageEncoder = Dropout(0.4)(ImageEncoder)
	ImageEncoder = Dense(1024, activation='relu')(ImageEncoder)
	ImageEncoder = Dense(256, activation='relu')(ImageEncoder)
	Classifier = Dense(13, activation='softmax', name='classifier_output')(ImageEncoder)


	# Language Encoder
	LanguageEncoderInput = Input(shape=(max_length_caption,))
	LanguageEncoder = Embedding(vocab_size, 128, mask_zero=True)(LanguageEncoderInput)
	LanguageEncoder = Dropout(0.35)(LanguageEncoder)
	LanguageEncoder = Bidirectional(GRU(128, return_sequences=True, dropout=0.25))(LanguageEncoder) 
	LanguageEncoder = Bidirectional(GRU(128, return_sequences=True, dropout=0.25))(LanguageEncoder) 
	LanguageEncoder = Attention(max_length_caption)(LanguageEncoder)

	#Decoder
	Decoder = Add()([ImageEncoder, LanguageEncoder])
	Decoder = Reshape((1,256))(Decoder)
	Decoder = Bidirectional(GRU(128, return_sequences=True,dropout=0.25))(Decoder) 
	Decoder = Flatten()(Decoder)
	Decoder = Dropout(0.4)(Decoder)
	Decoder = Dense(1024, activation='relu')(Decoder)
	Decoder = Dropout(0.4)(Decoder)
	Decoder = Dense(500, activation='relu')(Decoder)

	FinalDecoder = Dense(vocab_size, activation='softmax', name='decoder_output')(Decoder)
	losses = {
		"classifier_output": "categorical_crossentropy",
		"decoder_output": "categorical_crossentropy",
	}

	lossWeights = {"classifier_output": 0.5, "decoder_output": 1.5}

	model = Model(inputs=[ImageInput, LanguageEncoderInput], outputs=[FinalDecoder, Classifier], name='Captioner')
	model.compile(loss=losses, loss_weights = lossWeights, optimizer=Adam(lr=5e-5,decay=1e-5))
	
	return model


def greedySearch(photo):
	in_text = 'startseq'
	for i in range(max_length_caption):
		sequence = [word_to_index[w] for w in in_text.split(' ') if w in word_to_index]
		sequence = pad_sequences([sequence], maxlen = max_length_caption)
		yhat = loaded_model.predict([photo,sequence],verbose=1)
		seq_yhat, cls_yhat = yhat
		seq_yhat = np.argmax(seq_yhat)
		cls_yhat+=cls_yhat
		
		word = index_to_word[seq_yhat]
		in_text+=' '+word
		if word == 'endseq':
			break
	cls_yhat = cls_yhat / (i+1)
	cls_yhat = np.argmax(cls_yhat)

	final = in_text.split()
	final = final[1:-1]
	final = ' '.join(final)

	result = {'caption': final,
			  'category':Categories_mapping[cls_yhat]}
	return result
