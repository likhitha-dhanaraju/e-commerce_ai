from django.urls import path
from ProductsScrapper import views

urlpatterns=[
	path('',views.ProductsView)
]