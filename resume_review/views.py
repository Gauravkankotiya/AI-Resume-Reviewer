from django.shortcuts import redirect, render


def home_page(request):
    return render(request, "home.html")
