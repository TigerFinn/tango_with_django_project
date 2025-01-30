from django.shortcuts import render
from django.http import HttpResponse

from random import choice

# Create your views here.

def index(request):
    context_dict = {"boldmessage":"Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {"boldmessage":"This page has been put together by Finlay"}
    
    return render(request, 'rango/about.html', context=context_dict)
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")

def tiger(request):
    tigerAttributes = ["Majestic","The Best","Orange","Better than Kapaburys"]
    context_dict = {"tigerMessage":choice(tigerAttributes), "finalMessage":"And in case I don't see you.... Good afternoon, good evening and goodnight"}

    return render(request, 'rango/tiger.html', context=context_dict)

def tiger2(request):
    context_dict = {"tigerMessage":"amazing and there's nothing else to say", "finalMessage":"I said there's nothing else to say"}
    return render(request, 'rango/tiger.html', context = context_dict)