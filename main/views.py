from django.shortcuts import render, HttpResponse
from .lib.product_match import main as scraper
# from django.http import JsonResponse
# from django.core import serializers
# from .lib.scraper import daraz_search, muncha_search
# import json
# Create your views here.

data = []
logo = {
  "0": {
    "name": "daraz",
    "logo": "https://laz-img-cdn.alicdn.com/images/ims-web/TB1eIwbmljTBKNjSZFuXXb0HFXa.png"
  },
  "1": {  
    "name": "sastodeal",
    "logo": 'https://www.sastodeal.com/0/media/css/frontend/images/logo.png'
  },
  "2": {
    "name": "nepbay",
    "logo": "https://nepbay.com/uploads/2018082815354524400.svg"
  },
  "3": {
    "name": "muncha",
    "logo": "https://www.muncha.com/assets/images/logo.gif"
  },
  "4": {
    "name": "Gyapu",
    "logo": "https://www.gyapu.com/806b0f041fef60968c877fe5b54014cb.svg"
  }
}
# def search(request, query):
#     data = daraz_search(query)
#     return JsonResponse(json.loads(data))
# for api based


def search(request):
    global data
    query = request.GET.get('q')
    if query:
        data.clear()
        data = scraper(query)
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
        'item': item,
        'logo': logo
    }
    return render(request, 'item/item.html', context)
