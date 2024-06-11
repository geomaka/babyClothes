from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Category, Product, Customer, Order, OrderItem, Review, Cart, CartItem
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    return render(request,'Frontend\homepage.html')

def sign_in(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST["confirm-password"]

        if password != password2:
             messages.error(request, "Passwords don't match")

        else:
            pass 

        if user_name and email and password and password2:
            hashed_password = make_password(password)
            user = Person.objects.create(user_name=user_name, email=email, password=hashed_password)
            print(user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request,"Enter all the fields")

    return render(request,'Frontend/signup.html')


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not email or not password:
            messages.error(request, "Please fill in all fields")
            return render(request, "Frontend/login.html")

        try:
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            person = None

        if person is not None:
            if check_password(password,person.password):
                user, created = User.objects.get_or_create(email=person.email,defaults={"password":password})
                if created:
                    user.set_password(password)
                    user.save()

                auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "User with this email does not exist")

    return render(request, "Frontend/login.html")

def log_out(request):
    logout(request)

    return render(request,"Frontend/login.html",{
        "message" : "Logged out"
    })


def contact(request):
    return render(request,"Frontend/contact.html")


def shop(request):
    return render(request,"Frontend/shop.html")

def about(request):
    return render(request,"Frontend/about.html")


def category(request):
    if request.method == "POST":
        names = request.POST.getlist('name[]')
        descriptions = request.POST.getlist('description[]')

        if names and descriptions:
            for i in range(len(names)):
                name = names[i]
                description = descriptions[i]
                Category.objects.create(name=name, description=description)
                print(category)
                return HttpResponseRedirect(reverse('add-product'))

        else:
            messages.error(request,"Fill all the fields")

    else:
        return render(request,"Frontend/category.html")

def product(request):
    if request.method == 'POST':
        categories = request.POST.getlist('category[]')
        names = request.POST.getlist('name[]')
        descriptions = request.POST.getlist('description[]')
        prices = request.POST.getlist('price[]')
        stocks = request.POST.getlist('stock[]')
        availables = request.POST.getlist('available[]')
        images = request.FILES.getlist('image[]')

        for i in range(len(names)):
            category = Category.objects.get(id=categories[i])
            name = names[i]
            description = descriptions[i]
            price = prices[i]
            stock = stocks[i]
            available = availables[i] == 'on'
            image = images[i] if i < len(images) else None

            Product.objects.create(
                category=category,
                name=name,
                description=description,
                price=price,
                stock=stock,
                available=available,
                image=image
            )
            # return HttpResponseRedirect(reverse('shop'))
    return render(request,"Frontend/product.html",{
        "categories" : Category.objects.all()
    })