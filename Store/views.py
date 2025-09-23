from django.shortcuts import render , redirect

from .models import Product, Category, Profile

from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
\
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q

import json

from cart.cart import Cart


def search(request):
    if request.method == 'POST':
        query = request.POST.get('searched', '').strip()
        
        if query:
            # Search in product name OR category name
            products = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(category__name__icontains=query)
            ).distinct()
            
            if products.exists():
                return render(request, "search.html", {'searched': products, 'query': query})
            else:
                messages.warning(request, f"No products found for '{query}'")
                return render(request, "search.html", {'searched': [], 'query': query})
        else:
            messages.error(request, "Please enter something to search.")
            return render(request, "search.html", {'searched': [], 'query': ''})
    else:
        return render(request, 'search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        
        current_user, created = Profile.objects.get_or_create(user=request.user)

        shipping_user, created = ShippingAddress.objects.get_or_create(user = request.user)
        
        form = UserInfoForm(request.POST or None, instance = current_user)

        shipping_form= ShippingForm(request.POST or None, instance = shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            
            form.save()
            shipping_form.save()

            messages.success(request, "User Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form': form, 'shipping_form': ShippingForm})
    else:
        messages.success(request, "You Must be Logged In!!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they filled out the form
        if request.method == 'POST':
            # DO stuff
            form = ChangePasswordForm(current_user, request.POST)
            # IS the form Valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated")
                login(request, current_user)
                return redirect('Update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request,"update_password.html", {'form':form})
    else:
        messages.success(request, "YOu Must be Logged In...")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You Must be Logged In!!")
        return redirect('home')
    

def category(request,foo):
    #Replace hyphens with spaces
    foo = foo.replace('-',' ')
    #Grab the category from the url
    try:
        # Lookup the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products ,'category':category})

    except:
        messages.success(request, ("That Category Doesn't Exist.."))
        return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk )
    return render(request,'product.html',{'product':product })

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products , 'category':category})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request, username=username ,password=password)
        if user is not None:
            login(request, user)

            # Do some shopping
            current_user= Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from databse
            saved_cart = current_user.old_cart
            # convert database string to python dic
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the dic
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You have been Logged In."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, Please try again!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out."))
    return redirect('home')

def register_user(request):
    if request.method == "POST": 
        form = SignUpForm(request.POST) 
        if form.is_valid(): 
            user=form.save()
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password1']  
            user = authenticate(username=username, password=password) 
            login(request, user)
            messages.success(request, ("You Have Registered Successfully!!"))
            messages.success(request, ("Please Fill Out Your User Info!!")) 
            return redirect('update_info') 
        else: 
            # messages.success(request, ("Whoops! There was a problem. please try again!!")) 
            # return redirect('register')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm() 
        return render (request, 'register.html', {'form':form})