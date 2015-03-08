from django.shortcuts import render

def home(request):
	return render(request, 'survival/home.html')

def random_curve(request):
	return True