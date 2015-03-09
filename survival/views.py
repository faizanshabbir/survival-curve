from django.shortcuts import render
from django.http import HttpResponse
from . import survival

def home(request):
	return render(request, 'survival/home.html')

def random_curve(request):
	return render(request, 'survival/random_curve.html')

def random_data(request):
	data = survival.random_data()
	return HttpResponse(data, content_type="application/json")