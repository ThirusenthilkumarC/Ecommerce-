from django.shortcuts import render, redirect
from .models import Product


def home(request):
    return render(request, "home.html")


def login(request):
    return render(request, "login.html")


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

        Product.objects.create(

            name=request.POST.get("name"),

            price=request.POST.get("price"),

            description=request.POST.get("description"),

            image=request.FILES.get("image"),

            status=request.POST.get("status")

        )

        return redirect("products")

    return render(request, "add_product.html")