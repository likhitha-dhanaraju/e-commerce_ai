from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser
#from DescriptionMatcher.serializers import UrlsSerializer
from django.http import HttpRequest, JsonResponse
from DescriptionMatcher.services.description_matcher import Descriptor
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
import re

def preprocess_request(request):
	if isinstance(request,HttpRequest):
		return Request(request,parsers=[FormParser])
	return request

@csrf_exempt
def DescriptionView(request):
	#request = preprocess_request(request)
	if request.method=='GET':
		url1 = request.GET['URL1']
		url2 = request.GET['URL2']
		url1 = re.sub(" ","",url1)
		url2 = re.sub(" ", "",url2)
		#bow_similarity_quotient = Descriptor(url1,url2).bow_similarity_quotient()
		#print("BOW similarity quotient obtained!")
		#hash_similarity_quotient = Descriptor(url1,url2).hash_similarity_quotient()
		#print("hash similarity quotient obtained!")
		#tf_idf_similarity_quotient = Descriptor(url1,url2).tf_idf_similarity_quotient()
		#print("tf_idf similarity quotient obtained!")
		#glove_similarity_quotient = Descriptor(url1,url2).glove_similarity_quotient()
		#print("glove similarity quotient obtained!")		
		#nnlm_similarity_quotient = Descriptor(url1,url2).nnlm_similarity_quotient()
		unse_similarity_quotient = Descriptor(url1, url2).unse_similarity_quotient()
		print("Universal Sentence Encoder quotient obtained!")
		#word2vec_similarity_quotient = Descriptor(url1,url2).word2vec_similarity_quotient()
		#print("word2vec similarity quotient obtained!")
		#fasttext_similarity_quotient = Descriptor(url1,url2).fasttext_similarity_quotient()
		laser_similarity_quotient  = Descriptor(url1, url2).laser_similarity_quotient()
		print("Laser similarity quotient obtained!")
		sbert_similarity_quotient = Descriptor(url1, url2).sbert_similarity_quotient()		
		print("SBERT similarity quotient obtained!")
	

		result = {
			"input":{
				"URL1":url1,
				"URL2":url2
			},

			"results":{
			#"bow_similarity_quotient" : bow_similarity_quotient,
			#"hash_similarity_quotient" : hash_similarity_quotient,
			#"tf_idf_similarity_quotient": tf_idf_similarity_quotient,
			"laser_similarity_quotient":laser_similarity_quotient,
			"sbert_similarity_quotient":sbert_similarity_quotient,
			#"glove_similarity_quotient" : glove_similarity_quotient,
			#"word2vec_similarity_quotient":word2vec_similarity_quotient,
			"unse_similarity_quotient" : unse_similarity_quotient,
			#"nnlm_similarity_quotient" : nnlm_similarity_quotient,
			#"fasttext_similarity_quotient":fasttext_similarity_quotient,
			},
		}

		return JsonResponse(result,safe=False)
