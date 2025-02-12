from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import PizzaForm, OrderForm
from .models import Pizza, PizzaSize, CrustType, Sauce, Cheese, Topping, Order

def index(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "index.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, "index.html")

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = firstname
            user.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, "index.html")
        
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def home(request):
    return render(request, "home.html") 

def menu(request):
    return render(request, "menu.html")

def payment(request):
    return render(request, "payment.html")

def contact(request):
    return render(request, "contact.html")

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = Pizza(
                user=request.user,
                size=form.cleaned_data['size'],
                crust=form.cleaned_data['crust'],
                sauce=form.cleaned_data['sauce'],
                cheese=form.cleaned_data['cheese']
            )
            pizza.save()
            pizza.toppings.set(form.cleaned_data['toppings'])
            request.session['pizza_id'] = pizza.id
            return redirect('delivery')
    else:
        form = PizzaForm()
    return render(request, 'create_pizza.html', {'form': form})

@login_required
def delivery_details(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            pizza_id = request.session.get('pizza_id')
            if not pizza_id:
                return redirect('create_pizza')
            
            pizza = get_object_or_404(Pizza, id=pizza_id)
            pizza.name = form.cleaned_data['name']
            pizza.address = form.cleaned_data['address']
            pizza.save()

            request.session['pizza_id'] = pizza.id 
            return redirect('order')
    else:
        form = OrderForm()
    return render(request, 'delivery.html', {'form': form})

@login_required
def order_confirmation(request):
    pizza_id = request.session.get('pizza_id')
    if not pizza_id:
        return redirect('create_pizza')
    
    pizza = get_object_or_404(Pizza, id=pizza_id)
    
    if 'pizza_id' in request.session:
        del request.session['pizza_id']
    
    messages.success(request, 'Your order has been placed successfully!')
    return render(request, 'order.html', {'pizza': pizza})

@login_required
def order_history(request):
    orders = Pizza.objects.filter(user=request.user).order_by('-id')
    return render(request, 'order_history.html', {'orders': orders})