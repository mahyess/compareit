import ast
import re, requests
from decimal import Decimal
from bs4 import BeautifulSoup
import lxml
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
import random
# import urllib2

stores = [
  {
    "name": "daraz",
    "logo": "https://laz-img-cdn.alicdn.com/images/ims-web/TB1eIwbmljTBKNjSZFuXXb0HFXa.png"
  },
  {  
    "name": "sastodeal",
    "logo": 'https://cdn.sastodeal.com/logo/stores/1/SDLogo_White-Logo.png'
  },
  {
    "name": "nepbay",
    "logo": "https://nepbay.com/uploads/2018082815354524400.svg"
  },
  {
    "name": "muncha",
    "logo": "https://www.muncha.com/assets/images/logo.gif"
  },
  {
    "name": "Gyapu",
    "logo": "https://www.gyapu.com/806b0f041fef60968c877fe5b54014cb.svg"
  }
]
url_list = {
    'Daraz': 'https://www.daraz.com.np/catalog/?q=', 
    'Sastodeal': 'https://www.sastodeal.com/catalogsearch/result/?q=', 
    'NepBay': 'https://nepbay.com/shopping/search?q=',
    'Muncha': 'http://www.shop.muncha.com/Search.aspx?MID=1&q=',
    'Gyapu': 'https://www.gyapu.com/api/search?q='
}

# daraz_search_results = []
# sastodeal_search_results = []
# nepbay_search_results = []
# muncha_search_results = []

search_results = []
def fetch(url, data=None):
    s = requests.Session()
    if data is None:
        return s.get(url).content
    else:
        return s.post(url, data=data).content


def daraz_search(query):
    try:
        URL = url_list['Daraz'] + query.replace(" ", "+")
        
        soup = BeautifulSoup(fetch(URL), 'lxml')
        scripts = soup.find_all('script')
        script = None
        for script in scripts:
            if ('window.pageData=' in str(script.string)):
                # daraz has search results in json string with 'window.pageData=' appended to it
                break
        
        data = script.string.replace('window.pageData=', '').strip()  # remove appended string
        data = json.loads(data)  # convert to json
        data = data['mods']['listItems']  # just need data inside this array/attribute, throw everything else

        for item in data:  # loop through this array
            search_results.append({
                "id": item['nid'],
                "details": {
                    "origin": stores[0],
                    "url": item['productUrl'],
                    "title": item['name'],
                    "image": item['image'],
                    "price": {
                        "selling_price": float(item['price']),
                        "marking_price": float(item['originalPrice']) if 'originalPrice' in item else None
                    } 
                }})  # append the results to search result for display
        
    except Exception as e:
        print(e)
        print('Daraz: Error in Connection')
        pass
        # return data

    # print('d done')

def sastodeal_search(query):
    try:
        URL = url_list['Sastodeal'] + query.replace(" ", "%20")

        soup = BeautifulSoup(fetch(URL), 'lxml')
        products = soup.find_all('div', {'class': 'product-item-info'})[:-1]

        for item in products:
            sp = item.find('span', {'data-price-type': "oldPrice"})
            if sp:
                sp = sp['data-price-amount']
            search_results.append({
                "id": random.randint(1,999),
                "details": {
                    "origin": stores[1],
                    "url": item.find('a', {'class': "product-item-link"})['href'],
                    "title": item.find('a', {'class': "product-item-link"}).string,
                    "image": item.find('img', {'class': "product-image-photo"})['src'],
                    "price": {
                        "selling_price": float(item.find('span', {'data-price-type': "finalPrice"})['data-price-amount']),
                        "marking_price": float(sp) if sp else 0
                    } 
                }
            })
            
    except Exception as e:
        print(e, 'here')
        print('Sastodeal: Error in Connection')
        pass

def nepbay_search(query):
    try:
        URL = url_list['NepBay'] + query.replace(" ", "+")
        s = requests.Session()

        soup = BeautifulSoup(fetch(URL), 'lxml')
        # print(soup)
        panels = soup.find_all('div', {'class': 'col-xs-6 col-sm-6 col-md-4 ncs-ad-list'})
        # print(panels)
        for idx,panel in enumerate(panels):
            # print(panel)
            link = panel.find('div', {'class': 'PicImgGrid'}).find('a')['href'] #working :)
            
            title = panel.find('h4').find('a').get_text()

            image = panel.find('div', {'class': 'PicImgGrid'}).find('img')['src']

            price = panel['data-filter']
            price = json.loads(price)

            search_results.append({
                "id": idx,
                "details": {
                    "origin": stores[2],
                    "url": link,
                    "title": title.strip(),
                    "image": image,
                    "price": {
                        "selling_price": float(price),
                        "marking_price": None
                    } 
                }})

    except:
        print('Nepbay: Error in Connection')

def muncha_search(query):
    try:
        URL = url_list['Muncha'] + query.replace(" ", "+")
        s = requests.Session()

        soup = BeautifulSoup(fetch(URL), 'lxml')
        panels = soup.find_all('div', {'class': 'panel panel-default'})
        for idx,panel in enumerate(panels):
            link = panel.find('a', {'class': 'product-img'})['href']

            title = panel.find('a', {'class': 'ItemsBrowse_Title'}).get_text()

            image = panel.find('a', {'class': 'product-img'}).find('img')['src']

            prices = panel.find('div', {'class': 'price-desc'}).get_text().strip()
            prices = ' '.join(prices.split())

            prices = prices.split()
            # print(prices)

            price_list = []
            for price in prices:
                price = price.replace(',','')
                price = price.replace('Rs.','')
                price_list.append(int(Decimal(price)))

            if len(price_list) is 1:
                price_list.append(None)

            search_results.append({
                "id": idx,
                "details": {
                    "origin": stores[3],
                    "url": link,
                    "title": title.strip(),
                    "image": image,
                    "price": {
                        "selling_price": float(price_list[0]),
                        "marking_price": price_list[1]
                    } 
                }})
    except:
        print('Muncha: Error in Connection')
        pass

def gyapu_search(query):
    try:
        URL = url_list['Gyapu'] + query.replace(" ", "%20")

        soup = fetch(URL)
        products = json.loads(soup)['data']['products']
        for item in products:
            for variant in item['variant']:
                search_results.append({
                    "id": variant['variant_type'][0]['value'] if len(variant['variant_type']) else item['_id'],
                    "details": {
                        "origin": stores[4],
                        "url": f"https://www.gyapu.com/detail/{item['url_key']}",
                        "title": f"{item['name']} + {variant['variant_type'][0]['value'] if len(variant['variant_type']) else ''}",
                        "image": f"https://www.gyapu.com/{item['image'][0]['document']['path']}",
                        "price": {
                            "selling_price": float(variant['price']),
                            "marking_price": float(variant['sales_price'])
                        } 
                    }
                })

    except Exception as e:
        print(e, 'here')
        print('Gyapu: Error in Connection')
        pass

def main(query):
    search_results.clear()
    daraz_search(query)
    sastodeal_search(query)
    muncha_search(query)
    nepbay_search(query)
    gyapu_search(query)

    return(search_results)

if __name__ == '__main__':
    main(query)
