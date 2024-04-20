import requests
import logging
import json
from dataclasses import dataclass, asdict
from typing import Optional
from icecream import install
install()

_logger = logging.getLogger(__name__)

@dataclass
class ProjectFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    category: Optional[str] = None  # Type of category ('member', 'customer', 'supplier', 'product', 'contact')
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names


class Dolibarrpy():
    url = 'https://dolibarr.example.com/api/index.php/'
    token = 'your token'
    timeout = 16
    debug = False

    def __init__(self, url, token, timeout, debug):
        self.url = url
        self.token = token
        self.timeout = timeout
        self.debug = debug

    def get_headers(self):
        return {
            'DOLAPIKEY': self.token,
            'Accept': 'application/json'
        }

    def post_headers(self):
        return {
            'DOLAPIKEY': self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


    def call_list_api(self, object, params={}):
        url = self.url + object
        headers = self.get_headers()
        response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        try:
            result = json.loads(response.text)
        except:
            _logger.error('LIST API ERROR: ' + object)
            result = response.text
        return result

    def call_get_api(self, object, objid):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=self.timeout)
        if self.debug:
            ic(url)
            ic(response)
        json_result = json.loads(response.text)

        return json_result

    def call_create_api(self, object, params={}):
        url = self.url + object
        headers = self.get_headers()
        response = requests.post(url, json=params, headers=headers, timeout=self.timeout)
        try:
            result = json.loads(response.text)
        except:
            _logger.error(response)
            _logger.error(response.text)
            result = response
        return result

    def call_action_api(self, object, objid, action, params={}):
        url = self.url + object + '/' + str(objid) + "/" + action
        headers = self.post_headers()
        response = requests.post(url, json=params, headers=headers, timeout=self.timeout)
        if self.debug:
            ic(url)
            ic(response)
        try:
            result = json.loads(response.text)
        except:
            raise Exception(response.text)
        return result

    def call_update_api(self, object, objid, params={}):
        url = self.url + object + '/' + str(objid)

        params.update({'id': int(objid)})
        headers = self.get_headers()
        response = requests.put(url, json=params, headers=headers, timeout=self.timeout)
        result = json.loads(response.text)

        return result

    def call_delete_api(self, object, objid):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()
        print(url)
        response = requests.delete(url, json={'id': objid}, headers=headers, timeout=self.timeout)
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
        order = self.get_order_by_id(order_id)
        links = order.get('linkedObjectsIds')
        if links:
            shipment_list = links.get('shipping')
        else:
            shipment_list = self.call_list_api('shipments', params={})
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

    def create_shipment_from_order(self, order_id, address_id=0, shipping_method_id=0, date_delivery=0, tracking_number=''):
        # This creates a complete fulfillment shipment for an order
        # get order
        order = self.get_order_by_id(order_id)
        # set defaults
        shipment_data = {
            'socid': order.get('socid'),
            "origin_type": "commande",
            "origin_id": str(order_id),
            'tracking_number': tracking_number,
            'date_delivery': date_delivery,
            'fk_delivery_address': address_id,
            'shipping_method_id': shipping_method_id,
            "sizeS": "0",  # trueDepth
            "sizeW": "0",  # trueWidth
            "sizeH": "0",  # trueHeight
            "weight": "0",
            "weight_units": "0",
            "size_units": "0",
            "entrepot_id": "1"
        }

        shiplines = []
        orderlines = order.get('lines')
        # loop through order lines and create shipment lines
        for oline in orderlines:
            if oline.get('product_type') != "0":
                # only ship products (not services)
                continue
            sline = {
                "origin_line_id": oline.get('id'),
                "fk_origin_line": oline.get('id'),
                "qty": oline.get('qty'),
                "qty_shipped": oline.get('qty'),
                "fk_product": oline.get('fk_product'),
                "qty_asked": oline.get('qty'),
                "ref": oline.get('ref'),
                "product_ref": oline.get('product_ref'),
                "libelle": oline.get('libelle'),
                "product_label": oline.get('libelle'),
                "desc": oline.get('desc'),
                "product_desc": oline.get('description'),
                "description": oline.get('description'),
                "fk_origin": "orderline",
                "entrepot_id": "1"
            }
            shiplines.append(sline)

        #add lines to shipment
        shipment_data['lines'] = shiplines
        ship_id = self.call_create_api('shipments', shipment_data)
        return ship_id


    def set_shipment_to_validated(self, shipment_id):
        params = {
          "notrigger": 0
        }
        return self.call_action_api('shipments', shipment_id, 'validate', params=params)

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

    # PROJECTS
    def find_all_projects(self, with_status = ''):
        """
        Get projects with status
        @param status: 0 => draft, 1 => open, 2=> closed
        @return: list of projects
        """
        all_projects=[]
        page = 0
        some_projects = self.find_some_projects(with_status, page)
        while some_projects:
            all_projects = all_projects + list(some_projects)
            page += 1
            some_projects = self.find_some_projects(with_status, page)
            if len(some_projects) < 100:
                all_projects = all_projects + list(some_projects)
                break
        return all_projects

    def find_some_projects(self, with_status = '', page = 0):
        search_filter = ProjectFilter()
        if "draft" == with_status.lower():
            search_filter = ProjectFilter(
                page=page,
                sqlfilters="(t.fk_statut:=:0)"
            )
        if "open" == with_status.lower():
            search_filter = ProjectFilter(
                page=page,
                sqlfilters="(t.fk_statut:=:1)"
            )
        if "closed" == with_status.lower():
            search_filter = ProjectFilter(
                page=page,
                sqlfilters="(t.fk_statut:=:2)"
            )
        params = asdict(search_filter)
        result = self.call_list_api('projects', params=params)
        return result

    def get_project_by_id(self, objid):
        result = self.call_get_api('projects', objid=objid)
        return result

    def get_project_tasks_by_pid(self, objid, includetimespent=0):
        """
        Get project tasks based on project id
        @param includetimespent: 0 => Return only list of tasks, 1 => Include a summary of time spent, 2=> Include details of time spent lines
        @return: list of project tasks
        """
        objid = str(objid) + '/tasks?includetimespent=' + str(includetimespent)
        result = self.call_get_api('projects', objid)
        return result

    def get_project_roles_by_pid(self, objid, userid=0):
        """
        Get project roles based on project id
        @param userid: 0 => connected user, Any other number than 0 is interpretated as a user id and if that user has roles on that project, they are shown.
        @return: list of project roles
        """
        objid = str(objid) + '/roles?userid=' + str(userid)
        result = self.call_get_api('projects', objid)
        return result

