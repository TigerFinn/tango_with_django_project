from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

#Needed for tiger testing
from random import choice

# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}

    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {"boldmessage":"Finlay"}

    return render(request, 'rango/about.html', context=context_dict)
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        #Attempt to find category with the current slug
        category = Category.objects.get(slug=category_name_slug)
        
        #Retrieve pages
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category

    #Handle non-existent slugs
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    #Return a HTTP rendered version to the client
    return render(request, 'rango/category.html', context=context_dict)








#Views that I used to mess around with
def tiger(request):
    tigerAttributes = ["Majestic","The Best","Orange","Better than Kapaburys"]
    context_dict = {"tigerMessage":choice(tigerAttributes), "finalMessage":"And in case I don't see you.... Good afternoon, good evening and goodnight"}

    return render(request, 'rango/tiger.html', context=context_dict)

def tiger2(request):
    context_dict = {"tigerMessage":"amazing and there's nothing else to say", "finalMessage":"I said there's nothing else to say"}
    return render(request, 'rango/tiger.html', context = context_dict)