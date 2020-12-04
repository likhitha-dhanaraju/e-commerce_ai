import numpy as np
import cv2
from PIL import Image
import pandas as pd
import random
import json
import argparse
import sys
import os
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.initializers import glorot_uniform
from help_functions import *

parser = argparse.ArgumentParser(description='Image Captioning model')


parser.add_argument('--predict', action='store_true',
	 help='Argument to predict from the pre-trained model')
parser.add_argument('--model_path', type=str, default=None,
	help='Path to the pre-trained model')
parser.add_argument('--mapping_file', type=str,
	help='Path to the mapping file with the model')
parser.add_argument('--test_image', type=str, default=None,
	help='Path to the image to test')
parser.add_argument('--test_dir', type=str,default=None,
	help='Path to the test image directory')

parser.add_argument('--train', action='store_true',
	 help='Argument to train the model')
parser.add_argument('--annotation_path', default=None,
	help='Path to the annotations file for training')
parser.add_argument('--image_dir', default=None, 
	help='Path to the image dir')
parser.add_argument('--save_path', type=str,
		default=os.getcwd(), help='Path to save the model after training.')
parser.add_argument('--model_name', type=str,
		help='Name of the model to be saved.')
args = parser.parse_args()


if args.predict and args.train:
	raise ValueError("Choose either train or predict")

if args.predict and not args.model_path:
	raise ValueError("Please specify the model path of the pre-trained model")

if args.predict and not args.mapping_file:
	raise ValueError("Please specify the respective mapping file")

if args.predict:
	if not args.test_image or not args.test_dir:
		raise ValueError('Specify the test image path or the test directory path.') 

	if args.test_image or args.test_dir:
		raise ValueError("Specify either test image or test image directory")
if args.train and not args.annotation_path:
	raise ValueError("please specify the path for annotations")

if args.train and not args.image_dir:
	raise ValueError('Please specify the image directory for the images to train on.')

if args.train and not args.model_name:
	raise ValueError("please specify the model name to be saved as.")


if args.train:

	filename = args.annotation_path
	doc = load_doc(filename)
	print('Finished loading', filename)
	descriptions, categories = load_descriptions(doc)
	print('Loaded: %d ' % len(descriptions))
	clean_descriptions(descriptions)
	print("Finished cleaning descriptions")
	all_tokens = ' '.join(descriptions.values()).split()
	vocabulary = set(all_tokens)
	print('Vocabulary Size: %d' % len(vocabulary))
	unq_categories = set(categories.values())
	print('Number of categories: %d' % len(unq_categories))

	product_ids = list(descriptions.keys())
	random.shuffle(product_ids)
	train_product_ids = product_ids[:int(0.9*len(product_ids))]
	random.shuffle(train_product_ids)
	val_product_ids = product_ids[int(0.9*len(product_ids)):int(0.95*len(product_ids))]
	random.shuffle(val_product_ids)
	test_product_ids = product_ids[int(0.95*len(product_ids)):]
	random.shuffle(test_product_ids)

	
	train_captions = load_captions(descriptions,train_product_ids)
	val_captions = load_captions(descriptions, val_product_ids)
	test_captions = load_captions(descriptions, test_product_ids)

	### WORD TO INDEX DICTIONARY

	corpus = []
	for caption in val_captions+train_captions+test_captions:
		for token in caption.split():
			corpus.append(token)
			
	hash_map = Counter(corpus)
	vocab = []
	for token,count in hash_map.items():
			vocab.append(token)
			
	print('Number of original tokens',len(hash_map))
	print('Number of tokens after threshold',len(vocab))

	word_to_index = {}
	index_to_word = {}
		
	for idx,token in enumerate(vocab):
		word_to_index[token] = idx+1
		index_to_word[idx+1] = token

	vocab_size = len(index_to_word) + 1 # one for appended 0's
	max_length_caption = max_len_caption(train_captions+val_captions+test_captions)

	train_captions = load_captions_dict(descriptions,train_product_ids)
	val_captions = load_captions_dict(descriptions, val_product_ids)
	test_captions = load_captions_dict(descriptions, test_product_ids)

	train_features, train_product_ids = load_img_features(train_product_ids, args.image_dir)
	val_features, val_product_ids = load_img_features(val_product_ids, args.image_dir)

	# PREPROCESSING CATEGORIES


	encoded_data, mapping_index = pd.Series(list(unq_categories)).factorize()

	train_categories = load_categories_dict(categories, train_product_ids)
	val_categories = load_categories_dict(categories, val_product_ids)
	test_categories = load_categories_dict(categories, test_product_ids)

	model=model_def(max_length_caption, vocab_size)

	epochs = 50
	number_pics_per_batch = 128
	steps = len(train_captions)//number_pics_per_batch

	generator = data_generator(train_captions,  train_categories, train_features, word_to_index, max_length_caption, number_pics_per_batch)
	val_generator = data_generator(val_captions, val_categories, val_features, word_to_index,max_length_caption, number_pics_per_batch)
	output_dir = args.save_path

	reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, verbose=1,min_lr=1e-7, factor = 0.5)

	if os.path.exists(output_dir) == False:
	  os.mkdir(output_dir)
	  
	history = model.fit_generator(generator, validation_data = val_generator, 
										validation_steps = len(val_captions)//number_pics_per_batch
										,epochs=epochs,
										#,epochs=1,
									steps_per_epoch=steps,
									verbose=1, 
								   callbacks=[reduce_lr], shuffle=True)

	if '.h5' in args.model_name:
		root_name = args.model_name.strip().split('.h5')[0]
	else:
		root_name = args.model_name

	model.save(os.path.join(output_dir, root_name+'.h5'))
	print(history.history.keys())
	 
	# summarize history for loss
	print('loss')
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('model total loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc='upper right')
	plt.show()

	print('decoder_output_loss')
	plt.plot(history.history['decoder_output_loss'])
	plt.plot(history.history['val_decoder_output_loss'])
	plt.title('model decoder loss')
	plt.ylabel('decoder loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc='upper right')
	plt.show()

	print('classifier_output_loss')
	plt.plot(history.history['classifier_output_loss'])
	plt.plot(history.history['val_classifier_output_loss'])
	plt.title('model classifier loss')
	plt.ylabel('classifier loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc='upper right')
	plt.show()


	encoded_data, mapping_index = pd.Series(list(unq_categories)).factorize()

	Categories_mapping = list(mapping_index)

	f= open(output_dir, root_name+'.json','w')
	data = {'word_to_index':word_to_index,
			'index_to_word':index_to_word,
			'categories_mapping':Categories_mapping}
	json.dump(data,f)
	f.close()

if args.predict:

	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
			loaded_model = load_model(args.model_path, 
				custom_objects={'Attention':Attention})

	f = open(args.mapping_file,'r')

	data = json.load(f)
	word_to_index = data['word_to_index']
	index_to_word = data['index_to_word']
	Categories_mapping = data['categories_mapping']


	if args.test_image:

		in_layer = Input(shape=(224, 224, 3))
		model = VGG16(include_top=False, input_tensor=in_layer)

		image=  load_img(args.test_image,target_size=(224, 224,3))
		image = img_to_array(image)
		image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
		image = preprocess_input(image)
		test_image = model.predict(image, verbose=0)

		in_text = 'startseq'

		max_length_caption = 13

		for i in range(max_length_caption):
			sequence = [word_to_index[w] for w in in_text.split(' ') if w in word_to_index]
			sequence = pad_sequences([sequence], maxlen = max_length_caption)
			yhat = loaded_model.predict([image,sequence],verbose=1)
			seq_yhat, cls_yhat = yhat
			seq_yhat = np.argmax(seq_yhat)
			cls_yhat+=cls_yhat
			
			word = index_to_word[str(seq_yhat)]
			in_text+=' '+word
			if word == 'endseq':
				break
		cls_yhat = cls_yhat / (i+1)
		cls_yhat = np.argmax(cls_yhat)

		final = in_text.split()
		final = final[1:-1]
		final = ' '.join(final)

		result = {'caption':final,
				  'category':Categories_mapping[cls_yhat]}

		print(result)

	if args.test_dir:

		test_product_ids = os.listdir(args.test_dir)
		test_features, test_product_ids = load_img_features(test_product_ids)

		for i in range(len(test_product_ids)):
			pic= test_product_ids[i]
			print(pic)
			image = test_features[pic].reshape(1,7,7,512)
			cv2.imshow(pic,cv2.imread(args.test_dir+'/'+pic+'.jpg'))
			result = greedySearch(image, loaded_model, word_to_index, index_to_word, Categories_mapping)

			print(result)