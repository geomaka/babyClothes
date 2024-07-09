from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Category, Product, Customer, Order, OrderItem, Review, Cart, CartItem
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal


def index(request):
    return render(request,'Frontend/homepage.html')

def sign_in(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
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
                user, created = User.objects.get_or_create(email=person.email,defaults={"password":password},username=person.user_name)
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
    products = Product.objects.filter(available=True)
    return render(request, "Frontend/shop.html", {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    person, created = Person.objects.get_or_create(user_name=request.user.username, email=request.user.email)
    customer, created = Customer.objects.get_or_create(user=person)
    
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,quantity=1)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('shop')

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
            return HttpResponseRedirect(reverse('shop'))
    return render(request,"Frontend/product.html",{
        "categories" : Category.objects.all()
    })

@login_required
def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user.id)
    cart = get_object_or_404(Cart, customer=customer)
    total_price = 0
    
    for item in cart.items.all():
        total_price += item.product.price * item.quantity
    
    return render(request, 'Frontend/view_cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def place_order(request):
    customer = get_object_or_404(Customer, user=request.user.id)
    cart = get_object_or_404(Cart, customer=customer)
    
    order = Order.objects.create(customer=customer, status='Pending')
    total_price = Decimal('0.00')
    
    for cart_item in cart.items.all():
        item_price = cart_item.product.price * cart_item.quantity
        total_price += item_price

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=item_price
        )
    
    cart.items.all().delete
    
    send_order_confirmation_email(request.user.email, order)
    send_seller_notification_email(order)

    messages.success(request, 'Your order has been placed successfully!')
    return render(request,'Frontend/order_confirmation.html') 


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()

    return redirect('order_detail', order_id=order.id)

def send_order_confirmation_email(customer_email, order):
    subject = 'Order Confirmation'
    html_message = render_to_string('Frontend/order_confirmation.html', {'order': order})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, None, [customer_email], html_message=html_message)

def send_seller_notification_email(order):
    sellers_emails = [seller.email for seller in User.objects.filter(is_staff=True)]
    subject = f'New Order: #{order.id} from {order.customer.user.user_name}'
    html_message = render_to_string('Frontend/seller_notification.html', {'order': order})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, None, sellers_emails, html_message=html_message)