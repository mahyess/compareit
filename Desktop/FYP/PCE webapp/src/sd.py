import urllib.parse as urlparse
from urllib.parse import urlencode
import requests
import json

url = 'https://y942squ1t6-3.algolianet.com/1/indexes/*/queries?'
_params = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.21.1;instantsearch.js 1.11.15;JS Helper 2.19.0",
            "x-algolia-application-id": "Y942SQU1T6",
            "x-algolia-api-key": "849f864925ae4100bfe5863e46712b33"
        }

url_parts = list(urlparse.urlparse(url))
query = dict(urlparse.parse_qsl(url_parts[4]))
query.update(_params)

url_parts[4] = urlencode(query)

print(urlparse.urlunparse(url_parts))


with requests.Session() as session:
    _data = json.dumps(
        {"requests":
            [
                {
                    "indexName": "sastodeal_products",
                    'query': 'apple',
                }
            ]
        }
    )

    response = session.post(urlparse.urlunparse(url_parts), data=_data)

    j = json.loads(response.content)
    j = json.dumps(j, sort_keys=True, indent=4)

    # print(j)
