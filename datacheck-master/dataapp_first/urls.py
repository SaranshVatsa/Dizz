from django.urls import path
from . import views

urlpatterns = [
	path('', views.graph, name='graph'),
	path('docaccess', views.docaccess, name='docaccess')
]
