from django.urls import path
from NameGenerator import views

urlpatterns=[
	path('caption/',views.CaptionGenerator.as_view())
]