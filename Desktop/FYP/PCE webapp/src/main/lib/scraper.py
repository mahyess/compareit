import ast
import re, requests
from decimal import Decimal
from bs4 import BeautifulSoup
import lxml
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
# import urllib2

stores = ['Daraz', 'Sastodeal', 'NepBay', 'Muncha']
url_list = {
    'Daraz': 'https://www.daraz.com.np/catalog/?q=', 
    'Sastodeal': 'https://www.sastodeal.com/search.html?q=', 
    'NepBay': 'https://nepbay.com/shopping/search?q=',
    'Muncha': 'http://www.shop.muncha.com/Search.aspx?MID=1&q='}

# daraz_search_results = []
# sastodeal_search_results = []
# nepbay_search_results = []
# muncha_search_results = []

search_results = []

# def daraz_search(query):
#     req = requests.get(url_list['Daraz'])
#     soup = BeautifulSoup(req.content, 'lxml')
#     print(soup)

#     URL = url_list['Daraz'] + query.replace(" ", "+")
#     s = requests.Session()

#     def fetch(url, data=None):
#         if data is None:
#             return s.get(url).content
#         else:
#             return s.post(url, data=data).content

#     soup = BeautifulSoup(fetch(URL), 'lxml')
#     print(soup.prettify())
#     skus = soup.find_all('div', {'data-qa-locator': 'product-item'})
#     # searchfield = soup.find('input', {'id': 'header-search-input'})
#     for idx,sku in enumerate(skus):
#         print(sku)
#         # for link
#         link = sku.find('a', {'class': 'link'})['href'] #working :)

#         # for image
#         # imagediv = sku.find('div', {'class': 'image-wrapper'})
#         image = sku.find('img')['src'] #working just fine ^_^

#         # for title
#         title = sku.find('img')['alt']
#         # title = title_h2.find('span', {'class': 'name'}).get_text() #working as charm ;)

#         # for price
#         price_div = sku.find('div', {'price-container'}).find('span', {'class': 'price-box'})
#         price_spans = price_div.find_all('span', {'dir': 'ltr'})

#         prices = []
#         for price_span in price_spans:
#             prices.append(price_span['data-price']) #donejo working \m/
#         # one or two values may be present
#         # if one, that's the selling price
#         # if two, one is selling price, other is marked price

#         if len(prices) is 1:
#             prices.append(None)

#         daraz_search_results.append({
#             "id": idx, 
#             "url": link,
#             "title": title,
#             "image": image,
#             "price": {
#                 "selling_price": prices[0],
#                 "marking_price": prices[1]
#             } 
#         })
#     print(daraz_search_results)
#     return daraz_search_results
       
    # pass

def daraz_search(query):
    # req = requests.get(url_list['Daraz'])
    # soup = BeautifulSoup(req.content, 'lxml')
    # print(soup)
    try:
        URL = url_list['Daraz'] + query.replace(" ", "+")
        s = requests.Session()

        def fetch(url, data=None):
            if data is None:
                return s.get(url).content
            else:
                return s.post(url, data=data).content

        soup = BeautifulSoup(fetch(URL), 'lxml')
        # print(soup.prettify())
        scripts = soup.find_all('script')
        # for i in scripts:
        #     print(i)
        #     print('---------------')
        script = str(scripts[2].get_text()).replace('window.pageData=', '').strip()
        # script = script.encode("utf-8")
        
        _script = json.dumps(script, sort_keys=True, indent=4, separators=(',', ': '))
        _data = json.loads(json.loads(_script))
        data = _data['mods']['listItems']

        for item in data:
            search_results.append({
                "id": item['nid'],
                "details": {
                    "origin": 0,
                    "url": item['productUrl'],
                    "title": item['name'],
                    "image": item['image'],
                    "price": {
                        "selling_price": float(item['price']),
                        "marking_price": float(item['originalPrice'])
                    } 
                }})

        # return data
    except:
        print('Daraz: Error in Connection')
        pass
        # return data

    # print('d done')

def sastodeal_search(query):
    try:
        URL = url_list['Sastodeal'] + query.replace(" ", "%20")

        xhr_url = 'https://y942squ1t6-3.algolianet.com/1/indexes/*/queries?'
        _params = {
                "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.21.1;instantsearch.js 1.11.15;JS Helper 2.19.0",
                "x-algolia-application-id": "Y942SQU1T6",
                "x-algolia-api-key": "849f864925ae4100bfe5863e46712b33"
            }
        url_parts = list(urlparse.urlparse(xhr_url))
        q = dict(urlparse.parse_qsl(url_parts[4]))
        q.update(_params)

        url_parts[4] = urlencode(q)

        xhr_url = urlparse.urlunparse(url_parts)

        # xhr_url = 'https://y942squ1t6-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.21.1%3Binstantsearch.js%201.11.15%3BJS%20Helper%202.19.0&x-algolia-application-id=Y942SQU1T6&x-algolia-api-key=849f864925ae4100bfe5863e46712b33'
        with requests.Session() as session:
            session.get(URL)
            
            _data =json.dumps({"requests":
                [
                    {
                        "indexName": "sastodeal_products",
                        'query': query,
                    }
                ]
            })

            response = session.post(xhr_url, data=_data)
            # print(response.content)

            j = json.loads(response.content)
            sastodeal_search_unclean = json.dumps(j, sort_keys=True, indent=4)
            # print(sastodeal_search_unclean)
            
            _sastodeal_search = json.loads(sastodeal_search_unclean)
            # print(type(sastodeal_search))


            data = _sastodeal_search['results'][0]['hits']

            for item in data:
                search_results.append({
                    "id": item['id'],
                    "details": {
                        "origin": 1,
                        "url": "https://www.sastodeal.com/sastodeal/pr--" + item['pilId'],
                        "title": item['name'],
                        "image": item['image'],
                        "price": {
                            "selling_price": float(item['price']),
                            "marking_price": item['mrp']
                        } 
                    }})

            # return sastodeal_search['results']
    except:
        print('Sastodeal: Error in Connection')
        pass

def nepbay_search(query):
    try:
        URL = url_list['NepBay'] + query.replace(" ", "+")
        s = requests.Session()

        def fetch(url, data=None):
            if data is None:
                return s.get(url).content
            else:
                return s.post(url, data=data).content

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
                    "origin": 2,
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

        def fetch(url, data=None):
            if data is None:
                return s.get(url).content
            else:
                return s.post(url, data=data).content

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
                    "origin": 3,
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

def main(query):
    # query = input('Enter Search Query:')
    daraz_search(query)
    sastodeal_search(query)
    muncha_search(query)
    nepbay_search(query)

    # print(search_results)

    return(search_results)

if __name__ == '__main__':
    main(query)
