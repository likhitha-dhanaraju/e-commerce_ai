from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from ProductsScrapper.services.website_matcher import WebsiteMatcher

def preprocess_request(request):
	if isinstance(request,HttpRequest):
		return Request(request,parsers=[FormParser])
	return request

@csrf_exempt
def ProductsView(request):
	if request.method=='GET':
		url = request.GET['URL']
		result = WebsiteMatcher(url)

		if result==True:
			output = 'All the urls were successfully retreived'
		else:
			output = 'Some urls were missing'
		results = {
		"input": url,
		"output": output
		}

		return JsonResponse(results,safe=False)