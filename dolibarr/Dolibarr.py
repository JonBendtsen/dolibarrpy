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

    def call_action_api(self, object, objid, action, params={}):
        url = self.url + object + '/' + str(objid) + "/" + action
        headers = self.get_headers()
        response = requests.post(url, json=params, headers=headers, timeout=8)
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

    def call_delete_api(self, object, objid):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()
        print(url)
        response = requests.delete(url, json={'id': objid}, headers=headers, timeout=8)
        try:
            result = json.loads(response.text)
        except:
            result = False
        return result

    def get_orders_by_status(self, status):
        """
        Get orders by status
        @param status: 0 => draft, 1 => validated
        @return: list of orders
        """
        params = {
            'limit': 500,
            'sqlfilters': "(fk_statut:=:{})".format(status)
        }

        result = self.call_list_api('orders', params=params)
        return result

    def get_order_by_id(self, objid):
        result = self.call_get_api('orders', objid=objid)
        return result

    # SHIPMENTS
    def get_shipment_by_id(self, objid):
        result = self.call_get_api('shipments', objid=objid)
        return result

    def update_shipment_tracking(self, objid, tracking_id, shipping_method=0):
        params = {
            'tracking_number': tracking_id
        }

        if shipping_method:
            params.update({'shipping_method_id': shipping_method})

        self.call_update_api('shipments', objid, params=params)

    def get_shipments_by_orderid(self, order_id):
        shipment_list = self.get_order_by_id(order_id).get('linkedObjectsIds').get('shipping')
        shipments = []
        for item in shipment_list:
            ship = self.get_shipment_by_id(shipment_list[item])
            shipments.append(ship)
        return shipments

    def get_shipments_by_status(self, status):
        """
        Get shipments by status
        @param status: 0 => draft, 1 => validated
        @return: list of shipments
        """
        params = {
            'limit': 500,
            'origin_id': 440,
            'sqlfilters': "(fk_statut:=:{})".format(status)
        }

        # and (fk_shipping_method:=:9)
        erp_shipments = self.call_list_api('shipments', params=params)
        return erp_shipments

    def set_shipment_to_validated(self, shipment_id):
        params = {
          "notrigger": 0
        }
        return self.call_action_api('shipment', shipment_id, 'validate', params=params)

    # ORDERS
    def set_order_to_draft(self, order_id, idwarehouse=1):
        params = {
          "idwarehouse": idwarehouse
        }
        return self.call_action_api('orders', order_id, 'settodraft', params=params)

    def set_order_to_validated(self, order_id, idwarehouse=1):
        params = {
          "idwarehouse": idwarehouse
        }
        return self.call_action_api('orders', order_id, 'validate', params=params)

    # PRODUCTS
    def get_product_by_id(self, objid, includestockdata=1):
        if includestockdata == 1:
            objid = str(objid) + '?includestockdata=1'
        result = self.call_get_api('products', objid=objid)
        return result

    # Factory
    def get_factory_order_by_id(self, objid):
        result = self.call_get_api('factory', objid=objid)
        return result

