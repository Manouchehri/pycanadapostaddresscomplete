#!/usr/bin/python3

__author__ = 'David Manouchehri (david@davidmanouchehri.com)'

import urllib.request
import urllib.parse
import gzip
import json

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}

base_url = 'https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/json3ex.ws?'

key = 'HT97-HU28-TJ75-KE42'  # This is the public access key, replace with your own.

base_params = {'Key': key,
               '$cache': 'true'}

search_params = {'Key': key,
                 'Country': 'CAN',
                 'SearchTerm': '',
                 'LanguagePreference': 'en',
                 'LastId': '',
                 'SearchFor': 'Everything',
                 'OrderBy': 'UserLocation',
                 '$block': 'true',
                 '$cache': 'true'}

if __name__ == "__main__":
    import sys
    search_params['SearchTerm'] = ' '.join(sys.argv[1:]).strip()
    print(search_params['SearchTerm'])

url = base_url + urllib.parse.urlencode(search_params)


def grab_url_data(url):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    if response.info().get('Content-Encoding') == 'gzip':
        page_data = gzip.decompress(response.read())
    elif response.info().get('Content-Encoding') == 'deflate' or not response.info().get('Content-Encoding'):
        page_data = response.read()
    elif response.info().get('Content-Encoding'):
        print('Encoding type unknown')  # Probably should raise an exception.
    return page_data


data = grab_url_data(url).decode('utf-8')

parsed = json.loads(data)
print(parsed)
print(json.dumps(parsed, indent=4))