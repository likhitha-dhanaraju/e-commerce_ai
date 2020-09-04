from django.shortcuts import render
from .apps import NamegeneratorConfig

# Create your views here.
from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import cv2
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import default_storage
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input
import numpy as np

def preprocess_request(request):
	if isinstance(request,HttpRequest):
		return Request(request,parsers=[FormParser])
	return request


class CaptionGenerator(APIView):
	def get(self,request):
		if request.method == 'GET':

			f = request.FILES["image"]
			file_name = 'test.png'

			file_name_2 = default_storage.save(file_name, f)
			file_url = default_storage.url(file_name_2)
			original = load_img(file_url, target_size=(224, 224))
			image = img_to_array(original)

			image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

			image = preprocess_input(image)

			in_layer = Input(shape=(224, 224, 3))
			vggmodel = VGG16(include_top=False, input_tensor=in_layer)

			image = vggmodel.predict(image, verbose=0)
	
			model = NamegeneratorConfig.model

			in_text = 'startseq'

			f = open('mapping.json','r')

			data = json.load(f)
			word_to_index = data['word_to_index']
			index_to_word = data['index_to_word']
			Categories_mapping = data['categories_mapping']

			max_length_caption = 13

			for i in range(max_length_caption):
				sequence = [word_to_index[w] for w in in_text.split(' ') if w in word_to_index]
				sequence = pad_sequences([sequence], maxlen = max_length_caption)
				yhat = model.predict([image,sequence],verbose=1)
				seq_yhat, cls_yhat = yhat
				seq_yhat = np.argmax(seq_yhat)
				cls_yhat+=cls_yhat
				
				word = index_to_word[str(seq_yhat)]
				in_text+=' '+word
				if word == 'endseq':
					break
			cls_yhat = cls_yhat / (i+1)
			cls_yhat = np.argmax(cls_yhat)
			result = {'category':Categories_mapping[cls_yhat]}

			final = in_text.split()
			final = final[1:-1]
			final = ' '.join(final)
			
			result['caption'] = final

			return JsonResponse(result)
			