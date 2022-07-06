from django.shortcuts import render


def company(request):
	return render(request, "company.html")


def orders(request):
	return render(request, "orders.html")


def products(request):
	return render(request, "products.html")