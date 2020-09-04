from rest_framework import serializers

class UrlsSerializer(serializers.ModelSerializer):
	url1 = serializers.CharField(max_length=1000)
	url2 = serializers.CharField(max_length=1000)

	

