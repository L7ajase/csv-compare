from django.http import HttpResponse
from django.shortcuts import render

def homepage (request):
    return render(request, 'home.html')
    #return HttpResponse("hello world")
def about (request):
    return render(request, 'about.html')
    #return HttpResponse("hello about about about about")
"""def compare (request):
    return render(request, 'compare.html')"""