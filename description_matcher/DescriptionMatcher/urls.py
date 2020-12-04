from django.urls import path
from DescriptionMatcher import views

urlpatterns = [
	path('',views.DescriptionView),
	]