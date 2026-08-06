from django.shortcuts import render

def login(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
def products(request):
    return render(request, "products.html")