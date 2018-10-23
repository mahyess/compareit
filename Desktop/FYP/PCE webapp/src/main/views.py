from django.shortcuts import render, HttpResponse
from .lib.product_match import main as scraper
# from django.http import JsonResponse
# from django.core import serializers
# from .lib.scraper import daraz_search, muncha_search
# import json
# Create your views here.

data = []

# def search(request, query):
#     data = daraz_search(query)
#     return JsonResponse(json.loads(data))
# for api based


def search(request):
    global data
    query = request.GET.get('q')
    if query:
        data = scraper(query)
        print(data)
        context = {
            'title': query,
            'data': data
        }
        return render(request, 'main/home.html', context)


def home(request):
    if "q" in request.GET:
        return search(request)

    context = {
        'title': 'Home',
    }
    return render(request, 'main/dashboard.html', context)


def product(request, id):
    if "q" in request.GET:
        return search(request)

    item = data[int(id)]
    context = {
        'title': item['title'],
        'item': item
    }
    return render(request, 'item/item.html', context)
