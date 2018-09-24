import requests
from bs4 import BeautifulSoup
import lxml
import json

stores = ['Daraz', 'Sastodeal', 'NepBay']
url_list = {
    'Daraz': 'https://www.daraz.com.np/', 
    'Sastodeal': 'https://www.sastodeal.com/', 
    'NepBay': 'https://nepbay.com/',}

daraz_search_results = []

def darazsearch(query):
    # req = requests.get(url_list['Daraz'])
    # soup = BeautifulSoup(req.content, 'lxml')
    # print(soup)

    URL = 'https://www.daraz.com.np/phones-tablets/?price=4000-100800&sort=popularity&dir=desc&q=samsung+s9'
    s = requests.Session()

    def fetch(url, data=None):
        if data is None:
            return s.get(url).content
        else:
            return s.post(url, data=data).content

    soup = BeautifulSoup(fetch(URL), 'lxml')
    # print(soup.prettify())
    skus = soup.find_all('div', {'class': 'sku'})
    # searchfield = soup.find('input', {'id': 'header-search-input'})
    for idx,sku in enumerate(skus):
        # print(sku)
        # for link
        link = sku.find('a', {'class': 'link'})['href'] #working :)

        # for title
        title_h2 = sku.find('h2', {'class': 'title'})
        title = title_h2.find('span', {'class': 'name'}).get_text() #working as charm ;)
        
        # for image
        imagediv = sku.find('div', {'class': 'image-wrapper'})
        image = imagediv.find('img', {'class': 'lazy'})['data-src'] #working just fine ^_^

        # for price
        price_div = sku.find('div', {'price-container'}).find('span', {'class': 'price-box'})
        price_spans = price_div.find_all('span', {'dir': 'ltr'})

        prices = []
        for price_span in price_spans:
            prices.append(price_span['data-price']) #donejo working \m/
        # one or two values may be present
        # if one, that's the selling price
        # if two, one is selling price, other is marked price

        if len(prices) is 1:
            prices.append(None)

        daraz_search_results.append({
            "id": idx, 
            "url": link,
            "title": title,
            "image": image,
            "price": {
                "selling_price": prices[0],
                "marking_price": prices[1]
            } 
        })
       
    # pass

def main():
    query = input('Enter Search Query:')
    darazsearch(query)

if __name__ == '__main__':
    main()
