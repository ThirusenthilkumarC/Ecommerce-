from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
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
    return render(request, "dashboard.html")


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
            return redirect("products")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {
        "form": form,
    })