from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore

from rango.forms import CategoryForm, PageForm
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect # type: ignore
from django.urls import reverse # type: ignore

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth.decorators import login_required

from datetime import datetime



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

    #Update visitor
    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)

    return response

def about(request):
    context_dict = {"boldmessage":"Finlay"}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

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

# @login_required
def add_category(request):
    if request.user.is_authenticated:
        form = CategoryForm()

        if request.method == 'POST':
            form = CategoryForm(request.POST)

            if form.is_valid():
                form.save(commit=True)
                return redirect('/rango/')
        else:
            print(form.errors)

        return render(request, 'rango/add_category.html', {'form':form})
    else:
        return redirect(reverse('rango:login'))
        

@login_required
def add_page(request, category_name_slug):
    if request.user.is_authenticated:

        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None

        if category is None:
            return redirect('/rango/')

        form = PageForm()

        if request.method == 'POST':
            form = PageForm(request.POST)

            if form.is_valid():
                if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()

                    return redirect(reverse('rango:show_category',
                                            kwargs={'category_name_slug':category_name_slug}))
                else:
                    print(form.errors)

        context_dict = {'form': form, 'category':category}
        return render(request, 'rango/add_page.html', context=context_dict)
    else:
        return redirect(reverse('rango:login'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled")
            
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'rango/login.html')



@login_required
def restricted(request):
    if request.user.is_authenticated:
        return render(request,'rango/restricted.html')
    else:
        return reverse('rango:login')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits









#Views that I used to mess around with
def tiger(request):
    tigerAttributes = ["Majestic","The Best","Orange","Better than Kapaburys"]
    context_dict = {"tigerMessage":choice(tigerAttributes), "finalMessage":"And in case I don't see you.... Good afternoon, good evening and goodnight"}

    return render(request, 'rango/tiger.html', context=context_dict)

def tiger2(request):
    context_dict = {"tigerMessage":"amazing and there's nothing else to say", "finalMessage":"I said there's nothing else to say"}
    return render(request, 'rango/tiger.html', context = context_dict)