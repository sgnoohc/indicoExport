import hashlib
import hmac
import time
import requests
import os
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

#__________________________________________________________________________________________________________________________________
def build_indico_request(path, params, api_key=None, secret_key=None, only_public=False, persistent=False):
    # Building indico request url with the user API key
    items = list(params.items()) if hasattr(params, 'items') else list(params)
    if api_key:
        items.append(('apikey', api_key))
    if only_public:
        items.append(('onlypublic', 'yes'))
    if secret_key:
        if not persistent:
            items.append(('timestamp', str(int(time.time()))))
        items = sorted(items, key=lambda x: x[0].lower())
        url = '%s?%s' % (path, urlencode(items))
        signature = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'),
                             hashlib.sha1).hexdigest()
        items.append(('signature', signature))
    if not items:
        return path
    return '%s?%s' % (path, urlencode(items))

#__________________________________________________________________________________________________________________________________
def get_threeweeks_json_from_category(categID):
    # Retrieve plus minus 1 week of information in json and writes it to "<categID>.json"
    API_KEY = '35129c98-2ccc-4412-a331-d6a17d7de85e'
    SECRET_KEY = 'ffd7251b-7ff3-493c-953a-d389bb7ba0a6'
    PATH = '/export/categ/{0:d}.json'.format(categID)
    PARAMS = {
        'from': '-7d',
        'to': '7d'
    }
    indico_request_url = "https://indico.cern.ch{0:s}".format(build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY))
    requested_json_result = requests.get(indico_request_url)
    the_json_I_want = requested_json_result.json()
    with open('{0}.json'.format(categID), 'w') as f:
        f.write(json.dumps(the_json_I_want, indent=4))

if __name__ == '__main__':

    get_threeweeks_json_from_category(6803)
