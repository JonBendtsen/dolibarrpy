import requests
import logging
import json

_logger = logging.getLogger(__name__)


class Dolibarr():
    url = 'https://example.com/api/index.php/'
    token = 'your token'

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_headers(self):
        return {
            'DOLAPIKEY': self.token,
            'Content-Type': 'application/json'
        }

    def call_list_api(self, object, params={}):
        url = self.url + object
        headers = self.get_headers()
        response = requests.get(url, params=params, headers=headers, timeout=8)
        try:
            result = json.loads(response.text)
        except:
            _logger.error('LIST API ERROR')
            result = response.text
        return result

    def call_get_api(self, object, objid):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=8)
        result = json.loads(response.text)

        return result

    def call_create_api(self, object, params={}):
        url = self.url + object
        headers = self.get_headers()
        response = requests.post(url, json=params, headers=headers, timeout=8)
        try:
            result = json.loads(response.text)
        except:
            _logger.error(response)
            _logger.error(response.text)
            result = response
        return result

    def call_delete_api(self, object, objid='TBD'):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()

        response = requests.post(url, json={'id': objid}, headers=headers, timeout=8)
        try:
            result = json.loads(response.text)
        except:
            _logger.error(response)
            _logger.error(response.text)
        return result

    def call_update_api(self, object, objid, params={}):
        url = self.url + object + '/' + str(objid)

        params.update({'id': int(objid)})
        headers = self.get_headers()
        response = requests.put(url, json=params, headers=headers, timeout=8)
        result = json.loads(response.text)

        return result

