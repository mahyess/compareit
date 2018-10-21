from django.shortcuts import render, HttpResponse
from .lib.product_match import main as scraper
from django.http import JsonResponse
from django.core import serializers
# from .lib.scraper import daraz_search, muncha_search
import json
# Create your views here.

data = []

def home(request):
    # data = None
    context = {
        'title' : 'Home',
    }
    return render(request, 'main/dashboard.html', context)

# def search(request, query):
#     data = daraz_search(query)
#     return JsonResponse(json.loads(data))
# for api based

def search(request, query):
    global data
    data = scraper(query)
    # print(data)
    context = {
        'title' : 'CompareIt' + ' - ' + 'Home',
        'data': data
    }
    return render(request, 'main/home.html', context)

def product(request, id):
    print(len(data))
    item = data[int(id)]
    context = {
        'title': 'CompareIt' + ' - ' + item['title'],
        'data': item
    }
    return render(request, 'item/item.html', context)