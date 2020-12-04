from django.urls import path
from ImageCaptioning import views

urlpatterns=[
	path('',views.CaptionGenerator.as_view())
]
