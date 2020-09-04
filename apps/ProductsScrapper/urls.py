from django.urls import path
from ProductsScrapper import views

urlpatterns=[
	path('list/',views.ProductsView)
]