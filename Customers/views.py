from django.shortcuts import render
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
    data = Product.objects.all()

    return render(request, "products.html", {
        "products": data
    })


def add_product(request):

    if request.method == "POST":

        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        status = request.POST.get("status")

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image=image,
            status=status
        )

    return render(request, "add_product.html")