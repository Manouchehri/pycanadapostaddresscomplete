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

base_site = 'https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/'
base_find_url = base_site + 'Find/v2.10/json3ex.ws?'
base_search_url = base_site + 'RetrieveFormatted/v2.10/json3ex.ws?'

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

retrieve_params = {'Key': key,
                   'Id': '',
                   'Source': '',
                   '$cache': 'true'}

if __name__ == "__main__":
    import sys
    search_params['SearchTerm'] = ' '.join(sys.argv[1:]).strip()
    print(search_params['SearchTerm'])


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


data = grab_url_data(base_find_url + urllib.parse.urlencode(search_params)).decode('utf-8')

parsed = json.loads(data)

print(json.dumps(parsed, indent=4))