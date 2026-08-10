from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Product
from .forms import ProductForm


def home(request):
    return render(request, "home.html")


def login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        error = "Invalid username or password. Please try again."

    return render(request, "login.html", {
        "error": error,
        "username": request.POST.get("username", "") if request.method == "POST" else "",
    })


def dashboard(request):

    products = Product.objects.all()

    total_products = products.count()

    # Use the existing `status` field to determine availability
    available = products.filter(status="Available").count()

    out_of_stock = products.filter(status="Out of Stock").count()

    return render(request, "dashboard.html", {
        "products": products,
        "total_products": total_products,
        "available": available,
        "out_of_stock": out_of_stock,
    })


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def products(request):

    products = Product.objects.all()

    return render(request, "products.html", {
        "products": products
    })


def add_product(request):

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect("products")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {
        "form": form,
    })