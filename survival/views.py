from django.shortcuts import render
from django.http import HttpResponse
from . import survival
import json

def home(request):
	return render(request, 'survival/home.html')

def random_curve(request):
	return render(request, 'survival/random_curve.html')

def random_data(request):
	data = survival.random_data()
	return HttpResponse(data, content_type="application/json")

def input_data(request):
	return render(request, 'survival/input_data.html')

def generate_curve(request):
	
	if request.method == 'POST':
		data = json.loads(request.body)
		time1 = data['time1']
		data1 = data['data1']
		time2 = data['time2']
		data2 = data['data2']

		return HttpResponse(json.dumps(time1), content_type="application/json")
	else:
		return HttpResponse(
            json.dumps({"nothing to see": "here"}),
            content_type="application/json"
        )