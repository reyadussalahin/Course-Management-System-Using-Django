from django.shortcuts import render


def index(request):
	return render(request, 'main/index.html', {})

def about(request):
	return render(request, 'main/about.html', {})
