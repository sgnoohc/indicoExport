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
def get_events_from_json(parent_categID, categID_settings={}):
    # Retrieve list of eventIDs (6 digit numbers) from "<categID>.json"
    the_json_file_for_the_categID = open('{0}.json'.format(parent_categID))
    loaded_json_file_for_the_categID = json.load(the_json_file_for_the_categID)
    list_of_events = []
    for item in loaded_json_file_for_the_categID['results']:
        # Filtering specific events based on its parent category ID
        # e.g. 26 <-- Higgs meetings, 5783 <-- SMP-VV, etc.
        pass_filter = False
        if item['categoryId'] in categID_settings.keys():
            pass_filter = True
        if not pass_filter:
            continue
        list_of_events.append([item['id'], categID_settings[item['categoryId']]])
    return list_of_events

#__________________________________________________________________________________________________________________________________
def download_event_ics(eventID, detail='events'):
    if detail == 'contributions':
        API_KEY = '35129c98-2ccc-4412-a331-d6a17d7de85e'
        SECRET_KEY = 'ffd7251b-7ff3-493c-953a-d389bb7ba0a6'
        PATH = '/export/event/{0}.ics'.format(eventID)
        PARAMS = {
                'detail': detail
        }
        indico_request_url_for_this_one_event = "https://indico.cern.ch{0:s}".format(build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY, persistent=True))
        print indico_request_url_for_this_one_event
        os.system("curl -s -o events/{}_{}.ics '{}'".format(eventID, detail, indico_request_url_for_this_one_event))
        API_KEY = '35129c98-2ccc-4412-a331-d6a17d7de85e'
        SECRET_KEY = 'ffd7251b-7ff3-493c-953a-d389bb7ba0a6'
        PATH = '/export/event/{0}.ics'.format(eventID)
        PARAMS = {
                'detail': 'sessions'
        }
        indico_request_url_for_this_one_event = "https://indico.cern.ch{0:s}".format(build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY, persistent=True))
        print indico_request_url_for_this_one_event
        os.system("curl -s -o events/{}_{}.ics '{}'".format(eventID, 'sessions', indico_request_url_for_this_one_event))
    API_KEY = '35129c98-2ccc-4412-a331-d6a17d7de85e'
    SECRET_KEY = 'ffd7251b-7ff3-493c-953a-d389bb7ba0a6'
    PATH = '/export/event/{0}.ics'.format(eventID)
    PARAMS = {
            'detail': 'events'
    }
    indico_request_url_for_this_one_event = "https://indico.cern.ch{0:s}".format(build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY, persistent=True))
    print indico_request_url_for_this_one_event
    os.system("curl -s -o events/{}_{}.ics '{}'".format(eventID, 'events', indico_request_url_for_this_one_event))

if __name__ == '__main__':

    categIDs_settings_of_interest = {
            7803 : 'contributions', # Tracking POG
            1576 : 'events'       , # Trigger Studies Group
            1358 : 'contributions', # Tracking DPG/POG
            5783 : 'contributions', # SMP-VV
            26   : 'contributions', # Higgs meetings
            3886 : 'contributions', # SMP General
            5784 : 'events'       , # VVV Working meeting
            677  : 'contributions', # CMS General Meeting
            }

    list_of_events = get_events_from_json(6803, categID_settings=categIDs_settings_of_interest)

    for event_id, detail_setting in list_of_events:
        download_event_ics(event_id, detail=detail_setting)
