from django.shortcuts import render, redirect
from .models import Product


# Login Page
def login(request):
    return render(request, "login.html")


# Dashboard Page
def dashboard(request):
    return render(request, "dashboard.html")


# Home Page
def home(request):
    return render(request, "masterpage.html")


# About Page
def about(request):
    return render(request, "about.html")


# Contact Page
def contact(request):
    return render(request, "contact.html")


# Products List
def products(request):
    all_products = Product.objects.all()
    return render(request, "products.html", {
        "products": all_products
    })


# Add Product
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )

        return redirect("product_list")

    return render(request, "add_product.html")