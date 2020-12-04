from django.shortcuts import render
from .apps import NamegeneratorConfig

import json
import cv2
import os
import numpy as np

from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import default_storage
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.layers import Input

def preprocess_request(request):
	if isinstance(request,HttpRequest):
		return Request(request,parsers=[FormParser])
	return request


class CaptionGenerator(APIView):

	def preprocess_request(request):

		if isinstance(request,HttpRequest):
			return Request(request,parsers=[FormParser])
		return request

	def get(self,request):

		if request.method == 'GET':

	
			f = request.FILES["image"]

			image_name = '~/test.png'

			file_name = default_storage.save(image_name, f)

			image_url = default_storage.url(file_name)

			original = load_img(image_url, target_size=(299, 299))
			image = img_to_array(original)

			image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

			image = preprocess_input(image)

			in_layer = Input(shape=(299, 299, 3))

			vggmodel = InceptionV3(include_top=False, input_tensor=in_layer, pooling='max')

			image = vggmodel.predict(image, verbose=0)
			image = image.reshape(1, 2, 2, 512)
			
			request = preprocess_request(request)

			model_name = request.data['model_name']

			mapping_file = request.data['mapping_filename']

			model = NamegeneratorConfig(model_name).model()
		
			in_text = 'startseq'

			f = open('ImageCaptioning/models/{}'.format(mapping_file),'r')

			data = json.load(f)
			word_to_index = data['word_to_index']
			index_to_word = data['index_to_word']
			categories_mapping = data['categories_mapping']
			max_length_caption = data['max_length_caption']

			if not max_length_caption:
				max_length_caption=13 

			for i in range(max_length_caption):
				sequence = [word_to_index[w] for w in in_text.split(' ') if w in word_to_index]
				sequence = pad_sequences([sequence], maxlen = max_length_caption)

				yhat = model.predict([image,sequence],verbose=0)
				seq_yhat, cls_yhat = yhat
				seq_yhat = np.argmax(seq_yhat)
				cls_yhat+=cls_yhat
				
				word = index_to_word[str(seq_yhat)]
				in_text+=' '+word
				if word == 'endseq':
					break
			cls_yhat = cls_yhat / (i+1)
			cls_yhat = np.argmax(cls_yhat)
			result = {'category':categories_mapping[cls_yhat]}

			final = in_text.split()
			final = final[1:-1]
			final = ' '.join(final)
			
			result['caption'] = final

			return JsonResponse(result)
			