import requests
import logging
import json, urllib
from dataclasses import dataclass, asdict, replace
from typing import Optional
from icecream import install
install()

_logger = logging.getLogger(__name__)

@dataclass
class CategoryFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    type: Optional[str] = None          # Type of category ('member', 'customer', 'supplier', 'product', 'contact')
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')

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

@dataclass
class countryFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    namefilter: Optional[str] = None    # To filter the countries by name
    lang: Optional[str] = None      # Code of the language the label of the countries must be translated to
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)

@dataclass
class stateFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    country: Optional[str] = None    # To filter the country id
    namefilter: Optional[str] = None    # To filter the states by name
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)

@dataclass
class MemberFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    typeid: Optional[str] = None        # only get members with this typeid
    category: Optional[int] = None        # only get members with this status: draft | unpaid | paid | cancelled
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')
    properties: Optional[str] = None    # Restrict the data returned to these properties. Ignored if empty. Comma separated list of properties names

@dataclass
class ThirdpartyFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    mode: Optional[int] = None          # Set to 1 to show only customers Set to 2 to show only prospects Set to 3 to show only those are not customer neither prospect Set to 4 to show only suppliers
    category: Optional[int] = None      # Use this param to filter list by category
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')
    properties: Optional[str] = None    # Restrict the data returned to these properties. Ignored if empty. Comma separated list of properties names

@dataclass
class ContactFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    thirdparty_ids: Optional[str] = None    # Thirdparty ids to filter contacts of (example '1' or '1,2,3')
    category: Optional[int] = None      # Use this param to filter list by category
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')
    includecount: Optional[int] = None      # Count and return also number of elements the contact is used as a link for
    includeroles: Optional[int] = None      # Includes roles of the contact
    properties: Optional[str] = None        # Restrict the data returned to these properties. Ignored if empty. Comma separated list of properties names

@dataclass
class SubscriptionFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')
    properties: Optional[str] = None    # Restrict the data returned to these properties. Ignored if empty. Comma separated list of properties names

@dataclass
class ProductFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None             # Dolibarr self inserts a default of 100 if you don't specify
    page: Optional[int] = None              # page number
    mode: Optional[int] = None              # Use this param to filter list (0 for all, 1 for only product, 2 for only service)
    category: Optional[int] = None          # Use this param to filter list by category
    sqlfilters: Optional[str] = None        # (t.email:like:'john.doe@example.com')
    ids_only: Optional[bool] = None         # Return only IDs of product instead of all properties (faster, above all if list is long)
    variant_filter: Optional[int] = None    # Use this param to filter list (0 = all, 1=products without variants, 2=parent of variants, 3=variants only)
    pagination_data: Optional[bool] = None  # If this parameter is set to true the response will include pagination data. Default value is false. Page starts from 0
    includestockdata: Optional[int] = None  # Load also information about stock (slower)

@dataclass
class ProductIdFilter():
    includestockdata:   Optional[int]   = None  # Load also information about stock (slower)
    includesubproducts: Optional[bool]  = None  # Load information about subproducts ### dolibarr v18.0.5 doesn't seem to supply this ###
    includeparentid:    Optional[bool]  = None  # Load also ID of parent product (if product is a variant of a parent product)
    includetrans:       Optional[bool]  = None  # Load also the translations of product label and description

@dataclass
class ProposalFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = 100
    page: Optional[int] = 0
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None        # Syntax example "(t.statut:=:1)
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class OrderFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Other criteria to filter answers separated by a comma. Syntax example "(t.ref:like:'SO-%') and (t.date_creation:
    sqlfilterslines: Optional[str] = None    # Other criteria to filter answers separated by a comma. Syntax example "(tl.fk_product:=:'17') and (tl.price:
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class InvoiceFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Other criteria to filter answers separated by a comma. Syntax example "(t.ref:like:'SO-%') and (t.date_creation:
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class ShipmentFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class InterventionFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class TicketFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)
    properties: Optional[str] = None        # Restrict the data returned to theses properties. Ignored if empty. Comma separated list of properties names

@dataclass
class UserFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    user_ids: Optional[str] = None
    category: Optional[int] = None      # only get members with this status: draft | unpaid | paid | cancelled
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
        if self.debug:
            ic(url)
            ic(params)
            ic(response)
        if '<Response [501]>' == str(response):
            _logger.error('LIST API ERROR: ' + str(response))
            raise Exception(str(response))
        try:
            result = json.loads(response.text)
        except:
            _logger.error('LIST API ERROR: ' + object)
            result = response.text
        return result

    def call_get_api(self, object, objid, params = None):
        url = self.url + object + '/' + str(objid)
        headers = self.get_headers()
        if params:
            dolibarrpy_response_call_get_api = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        else:
            dolibarrpy_response_call_get_api = requests.get(url, headers=headers, timeout=self.timeout)
        if self.debug:
            ic(url)
            ic(dolibarrpy_response_call_get_api)
            ic(dolibarrpy_response_call_get_api.text)
        try:
            result = json.loads(dolibarrpy_response_call_get_api.text)
        except json.decoder.JSONDecodeError:
            result = { "error": dolibarrpy_response_call_get_api }
        except:
            _logger.error('LIST API ERROR: ' + object)
            result = dolibarrpy_response_call_get_api.text
        return result

    def call_create_api(self, object, params={}):
        url = self.url + object
        headers = self.post_headers()
        dolibarrpy_response_call_create_api = requests.post(url, json=params, headers=headers, timeout=self.timeout)
        if self.debug:
            ic(url)
            ic(dolibarrpy_response_call_create_api)
        try:
            result = json.loads(dolibarrpy_response_call_create_api.text)
        except:
            _logger.error(dolibarrpy_response_call_create_api)
            _logger.error(dolibarrpy_response_call_create_api.text)
            result = dolibarrpy_response_call_create_api
        return result

    def call_action_api(self, object, objid, action, params={}):
        url = self.url + object + '/' + str(objid) + "/" + action
        headers = self.post_headers()
        response = requests.post(url, json=params, headers=headers, timeout=self.timeout)
        if self.debug:
            ic(url)
            ic(response)
        result = {}
        try:
            result = json.loads(response.text)
        except:
            try:
                response_code = response.status_code
            except:
                response_code = None
            try:
                response_text = response.text
            except:
                response_text = None
            result.update({ "response_code": response_code, "response_text": response_text })
        return result

    def call_post_api(self, object, objid):
        url = self.url + object + '/' + str(objid)
        if self.debug:
            ic()
            ic(object)
            ic(objid)
            ic(url)

        params = {}
        params.update({'id': int(objid)})
        headers = self.post_headers()
        response = requests.post(url, json=params, headers=headers, timeout=self.timeout)
        result = json.loads(response.text)

        return result

    def call_update_api(self, object, objid, params={}, extra_object=None, extra_id=None):
        if self.debug:
            ic()
            ic(object)
            ic(objid)
            ic(params)
            ic(extra_object)
            ic(extra_id)

        if objid:
            url = self.url + object + '/' + str(objid)
            params.update({'id': int(objid)})
        else:
            url = self.url + object

        if extra_object and extra_id:
            url = self.url + object + '/' + str(objid) + '/'  + extra_object + '/' + str(extra_id)

        headers = self.post_headers()
        if self.debug:
            ic(url)
            ic(headers)
        response = requests.put(url, json=params, headers=headers, timeout=self.timeout)

        if self.debug:
            ic(response)
            ic(response.text)
        try:
            result = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            result = { "error": response }
        except:
            _logger.error('LIST API ERROR: ' + object)
            result = response.text
        return result

    def call_delete_api(self, object, objid):
        if '' == object:
            url = self.url + str(objid)
        else:
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
        @endpoint 'get /orders'
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
        """
        @endpoint 'get /orders/{id}'
        """
        result = self.call_get_api('orders', objid=objid)
        return result

    # SHIPMENTS
    def find_all_shipments(self, from_ShipmentFilter = None):
        """
        @endpoint 'get /shipments'
        Get all shipments
        @param from_ShipmentFilter:
        @return: list of a shipments
        """
        if self.debug:
            ic()
            ic(from_ShipmentFilter)
        if from_ShipmentFilter is None:
            search_filter = ShipmentFilter()
        else:
            search_filter = from_ShipmentFilter
        all_shipments=[]
        page = 0
        while True:
            some_shipments = self.find_some_shipments(search_filter, page)
            if "error" in some_shipments:
                break
            elif [] == some_shipments:
                break
            elif {} == some_shipments:
                break
            else:
                page += 1
                if some_shipments == all_shipments:
                    break
                all_shipments = all_shipments + list(some_shipments)
        return all_shipments

    def find_some_shipments(self, from_ShipmentFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ShipmentFilter)
        if from_ShipmentFilter is None:
            search_filter = ShipmentFilter()
        else:
            search_filter = from_ShipmentFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('shipments', params)
        return result

    def get_shipment_by_id(self, objid):
        """
        @endpoint 'get /shipments/{id}'
        """
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
        """
        @endpoint 'get /orders/{id}/shipment'
        """
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
        @endpoint 'get /shipments'
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
        """
        @endpoint 'post /orders/{id}/shipment/{warehouse_id}'
        """
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
        """
        @endpoint 'post /shipments/{id}/validate'
        """
        params = {
          "notrigger": 0
        }
        return self.call_action_api('shipments', shipment_id, 'validate', params=params)

    # ORDERS
    def set_order_to_draft(self, order_id, idwarehouse=1):
        """
        @endpoint 'post /orders/{id}/settodraft'
        """
        params = {
          "idwarehouse": idwarehouse
        }
        return self.call_action_api('orders', order_id, 'settodraft', params=params)

    def set_order_to_validated(self, order_id, idwarehouse=1, notrigger = 0):
        """
        @endpoint 'post /orders/{id}/validate'
        """
        params = {
          "idwarehouse": idwarehouse,
          "notrigger": notrigger
        }
        return self.call_action_api('orders', order_id, 'validate', params=params)

    # PRODUCTS
    def find_all_products_services(self, from_productFilter = None):
        """
        @endpoint 'get /products'
        Get all products and/or services
        @param from_productFilter:
        @return: list of a products and/or services
        """
        if self.debug:
            ic()
            ic(from_productFilter)
        if from_productFilter is None:
            search_filter = ProductFilter()
        else:
            search_filter = from_productFilter
        all_products=[]
        page = 0
        while True:
            some_products = self.find_some_products_services(search_filter, page)
            if "error" in some_products:
                break
            elif [] == some_products:
                break
            elif {} == some_products:
                break
            else:
                page += 1
                if some_products == all_products:
                    break
                all_products = all_products + list(some_products)
        return all_products

    def find_some_products_services(self, from_productFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_productFilter)
        if from_productFilter is None:
            search_filter = ProductFilter()
        else:
            search_filter = from_productFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('products', params)
        return result

    def find_only_products(self, from_productFilter = None):
        """
        @endpoint 'get /products'
        Get only products
        @param from_productFilter:
        @return: list of only products
        """
        if self.debug:
            ic()
            ic(from_productFilter)
        if from_productFilter is None:
            search_filter = ProductFilter(
                mode=1
            )
        else:
            from_productFilter.mode=1
            search_filter = from_productFilter
        only_products = self.find_some_products_services(search_filter)
        return only_products

    def find_only_services(self, from_productFilter = None):
        """
        @endpoint 'get /products'
        Get only services
        @param from_productFilter:
        @return: list of only services
        """
        if self.debug:
            ic()
            ic(from_productFilter)
        if from_productFilter is None:
            search_filter = ProductFilter(
                mode=2
            )
        else:
            from_productFilter.mode=2
            search_filter = from_productFilter
        only_services = self.find_some_products_services(search_filter)
        return only_services

    def get_product_by_id(self, objid, from_ProductIdFilter = None ):
        """
        @endpoint 'get /products/{id}'
        """
        if self.debug:
            ic()
            ic(objid)
            ic(from_ProductIdFilter)

        if from_ProductIdFilter is None:
            search_filter = ProductIdFilter()
        else:
            search_filter = from_ProductIdFilter
        params = asdict(search_filter)

        result = self.call_get_api('products', objid=objid, params=params)
        return result

    def get_product_by_ref(self, objref, from_ProductIdFilter = None ):
        """
        @endpoint 'get /products/{id}'
        """
        if self.debug:
            ic()
            ic(objref)
            ic(from_ProductIdFilter)

        if from_ProductIdFilter is None:
            search_filter = ProductIdFilter()
        else:
            search_filter = from_ProductIdFilter
        params = asdict(search_filter)

        result = self.call_get_api('products/ref', objid=objref, params=params)
        return result

    def create_order_from_proposal(self, objid):
        """
        @endpoint 'post /orders/createfromproposal/{proposalid}'
        Create an order using an existing proposal.
        @return: proposal
        """
        if self.debug:
            ic()
            ic(objid)
        objid = str(objid)
        result = self.call_post_api('orders/createfromproposal', objid=objid)
        return result

    # Factory
    def get_factory_order_by_id(self, objid):
        result = self.call_get_api('factory', objid=objid)
        return result

    # PROJECTS
    def find_all_projects(self, with_status = ''):
        """
        @endpoint 'get /projects'
        Get projects with status
        @param with_status: 0 => draft, 1 => open, 2=> closed
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
                sqlfilters="(t.fk_statut:=:0)"
            )

        if "open" == with_status.lower():
            search_filter = ProjectFilter(
                sqlfilters="(t.fk_statut:=:1)"
            )
        if "closed" == with_status.lower():
            search_filter = ProjectFilter(
                sqlfilters="(t.fk_statut:=:2)"
            )
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('projects', params=params)
        return result

    def get_project_by_pid(self, objid):
        """
        @endpoint 'get /projects/{id}'
        Get project based on project id
        @return: project 
        """
        result = self.call_get_api('projects', objid=objid)
        return result

    def get_project_tasks_by_pid(self, objid, includetimespent=0):
        """
        @endpoint 'get /projects/{id}/tasks'
        Get project tasks based on project id
        @param includetimespent: 0 => Return only list of tasks, 1 => Include a summary of time spent, 2=> Include details of time spent lines
        @return: list of project tasks
        """
        objid = str(objid) + '/tasks?includetimespent=' + str(includetimespent)
        result = self.call_get_api('projects', objid)
        return result

    def get_project_roles_by_pid(self, objid, userid=0):
        """
        @endpoint 'get /projects/{id}/roles'
        Get project roles based on project id
        @param userid: 0 => connected user, Any other number than 0 is interpretated as a user id and if that user has roles on that project, they are shown.
        @return: list of project roles
        """
        objid = str(objid) + '/roles?userid=' + str(userid)
        result = self.call_get_api('projects', objid)
        return result

    def get_project_by_ref(self, ref):
        """
        @endpoint 'get /projects/ref/{ref}'
        Get project tasks based on project ref
        @return: project
        """
        if ref:
            ref = 'ref/' + urllib.parse.quote(ref)
            result = self.call_get_api('projects', ref)
            return result
        elif ref == '':
            raise Exception("ref can not be empty")
        elif ref is None:
            raise Exception("ref can not be None")
        else:
            raise Exception("ref is wrong")

    def get_project_by_ref_ext(self, ref_ext):
        """
        @endpoint 'get /projects/ref_ext/{ref_ext}'
        Get project tasks based on project ref_ext
        @return: project
        """
        if ref_ext:
            ref_ext = 'ref_ext/' + urllib.parse.quote(ref_ext)
            result = self.call_get_api('projects', ref_ext)
            return result
        elif ref_ext == '':
            raise Exception("ref_ext can not be empty")
        elif ref_ext is None:
            raise Exception("ref_ext can not be None")
        else:
            raise Exception("ref_ext is wrong")

    def get_project_by_email_msgid(self, email_msgid):
        """
        @endpoint 'get /projects/email_msgid/{email_msgid}'
        Get project tasks based on project email_msgid
        @return: project
        """
        if email_msgid:
            email_msgid = 'email_msgid/' + urllib.parse.quote(email_msgid)
            result = self.call_get_api('projects', email_msgid)
            return result
        elif email_msgid == '':
            raise Exception("email_msgid can not be empty")
        elif email_msgid is None:
            raise Exception("email_msgid can not be None")
        else:
            raise Exception("email_msgid is wrong")


    # MEMBERS
    def find_all_members(self, from_MemberFilter = None):
        """
        @endpoint 'get /members'
        Get members with status
        @param from_MemberFilter: 0 => draft, 1 => open, 2=> closed
        @return: list of members
        """
        if self.debug:
            ic()
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        all_members=[]
        page = 0
        while True:
            some_members = self.find_some_members(search_filter, page)
            if "error" in some_members:
                break
            elif [] == some_members:
                break
            elif {} == some_members:
                break
            else:
                page += 1
                all_members = all_members + list(some_members)
        return all_members

    def find_some_members(self, from_MemberFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        result = self.call_list_api('members', params=params)
        return result

    def create_member(self, memberModel):
        """
        @endpoint 'post /members'
        Create member
        @memberModel     str     { request_data (Array[string], optional): Request data }
        @return: json with new member
        """
        if self.debug:
            ic()
            ic(memberModel)
        result = self.call_create_api('members', params=memberModel)
        return result

    def get_member_by_mid(self, objid):
        """
        @endpoint 'get /members/{id}'
        Get member based on member id
        @return: member
        """
        result = self.call_get_api('members', objid=objid)
        return result

    def get_member_subscriptions_by_mid(self, objid):
        """
        @endpoint 'get /members/{id}/subscriptions'
        Get member subscriptions based on member id
        @return: list of member subscriptions
        """
        objid = str(objid) + '/subscriptions'
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_id(self, objid):
        """
        @endpoint 'get /members/thirdparty/{thirdparty}'
        Get member based on thirdparty id
        @return: member
        """
        objid = 'thirdparty/' + str(objid)
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_barcode(self, barcode):
        """
        @endpoint 'get /members/thirdparty/barcode/{barcode}'
        Get member based on thirdparty barcode
        @return: member
        """
        objid = 'thirdparty/barcode/' + str(barcode)
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_email(self, email):
        """
        @endpoint 'get /members/thirdparty/email/{email}'
        Get member based on thirdparty email
        @return: member
        """
        objid = 'thirdparty/email/' + str(email)
        result = self.call_get_api('members', objid)
        return result

    def find_all_member_types(self, from_MemberFilter = None):
        """
        @endpoint 'get /members/types'
        Get member_types
        @param from_MemberFilter: 0 => draft, 1 => open, 2=> closed
        @return: list of member_types
        """
        if self.debug:
            ic()
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        all_member_types=[]
        page = 0
        while True:
            some_member_types = self.find_some_member_types(search_filter, page)
            if "error" in some_member_types:
                break
            elif [] == some_member_types:
                break
            elif {} == some_member_types:
                break
            else:
                page += 1
                all_member_types = all_member_types + list(some_member_types)
        return all_member_types

    def find_some_member_types(self, from_MemberFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        category = params.get("category")
        if category:
            raise Exception("sorry, you can not use category in this filter, try without")
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        typeid = params.get("typeid")
        if typeid:
            raise Exception("sorry, you can not use typeid in this filter, try without")
        result = self.call_list_api('members/types', params=params)
        return result

    def get_all_member_categories_by_mid(self, objid, from_MemberFilter = None):
        """
        @endpoint 'get /members/{id}/categories'
        Get all categories for a member
        @param from_MemberFilter:
        @return: list of a members categories
        """
        if self.debug:
            ic()
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        all_member_categories=[]
        page = 0
        while True:
            some_member_categories = self.get_some_member_categories_by_mid(objid, search_filter, page)
            if self.debug:
                ic(some_member_categories)
            if "error" in some_member_categories:
                break
            elif [] == some_member_categories:
                break
            elif {} == some_member_categories:
                break
            else:
                page += 1
                if some_member_categories == all_member_categories:
                    break
                all_member_categories = all_member_categories + list(some_member_categories)
        return all_member_categories

    def get_some_member_categories_by_mid(self, objid, from_MemberFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_MemberFilter)
        if from_MemberFilter is None:
            search_filter = MemberFilter()
        else:
            search_filter = from_MemberFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        category = params.get("category")
        if category:
            raise Exception("sorry, you can not use category in this filter, try without")
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        properties = params.get("properties")
        if properties:
            raise Exception("sorry, you can not use properties in this filter, try without")
        sqlfilters = params.get("sqlfilters")
        if sqlfilters:
            raise Exception("sorry, you can not use sqlfilters in this filter, try without")
        typeid = params.get("typeid")
        if typeid:
            raise Exception("sorry, you can not use typeid in this filter, try without")
        api_path = 'members/' + str(objid) + '/categories'
        result = self.call_list_api(api_path, params)
        if self.debug:
            ic(result)
        return result


    # THIRDPARTIES
    def find_all_thirdparty(self, from_ThirdpartyFilter = None):
        """
        @endpoint 'get /thirdparties'
        Get all thirdparties
        @param from_ThirdpartyFilter:
        @return: list of a thirdparties
        """
        if self.debug:
            ic()
            ic(from_ThirdpartyFilter)
        if from_ThirdpartyFilter is None:
            search_filter = ThirdpartyFilter()
        else:
            search_filter = from_ThirdpartyFilter
        all_thirdparty=[]
        page = 0
        while True:
            some_thirdparty = self.find_some_thirdparty(search_filter, page)
            if "error" in some_thirdparty:
                break
            elif [] == some_thirdparty:
                break
            elif {} == some_thirdparty:
                break
            else:
                page += 1
                if some_thirdparty == all_thirdparty:
                    break
                all_thirdparty = all_thirdparty + list(some_thirdparty)
        return all_thirdparty

    def find_some_thirdparty(self, from_ThirdpartyFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ThirdpartyFilter)
        if from_ThirdpartyFilter is None:
            search_filter = ThirdpartyFilter()
        else:
            search_filter = from_ThirdpartyFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('thirdparties', params)
        return result

    def create_thirdparties(self, thirdpartiesModel):
        """
        @endpoint 'post /thirdparties'
        Create thirdparty
        @thirdpartiesModel     str     { request_data (Array[string], optional): Request data }
        @return: json with new thirdparty
        """
        result = self.call_create_api('thirdparties', params=thirdpartiesModel)
        return result

    def get_thirdparty_by_tid(self, objid):
        """
        @endpoint 'get /thirdparties/{id}'
        Get thirdparty based on thirdparty id
        @return: thirdparty
        """
        result = self.call_get_api('thirdparties', objid=objid)
        return result

    def get_thirdparty_by_barcode(self, barcode):
        """
        @endpoint 'get /thirdparties/barcode/{barcode}'
        Get thirdparty from barcode
        @return: thirdparty
        """
        objid = 'barcode/' + str(barcode)
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparty_by_email(self, email):
        """
        @endpoint 'get /thirdparties/email/{email}'
        Get thirdparty based on thirdparty email
        @return: thirdparty
        """
        objid = 'email/' + str(email)
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_bankaccounts_by_tid(self, objid):
        """
        @endpoint 'get /thirdparties/{id}/bankaccounts'
        Get thirdparty bankaccounts based on thirdparty id
        @return: list of thirdparty bankaccounts
        """
        objid = str(objid) + '/bankaccounts'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_getinvoicesqualifiedforcreditnote_by_tid(self, objid):
        """
        @endpoint 'get /thirdparties/{id}/getinvoicesqualifiedforcreditnote'
        Get thirdparty invoices qualifiedforcreditnote based on thirdparty id
        @return: list of thirdparty invoices qualifiedforcreditnote
        """
        objid = str(objid) + '/getinvoicesqualifiedforcreditnote'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_getinvoicesqualifiedforreplacement_by_tid(self, objid):
        """
        @endpoint 'get /thirdparties/{id}/getinvoicesqualifiedforreplacement'
        Get thirdparty invoices qualifiedforreplacement based on thirdparty id
        @return: list of thirdparty invoices qualifiedforreplacement
        """
        objid = str(objid) + '/getinvoicesqualifiedforreplacement'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_notifications_by_tid(self, objid):
        """
        @endpoint 'get /thirdparties/{id}/notifications'
        Get thirdparty notifications based on thirdparty id
        @return: list of thirdparty notifications
        """
        objid = str(objid) + '/notifications'
        result = self.call_get_api('thirdparties', objid)
        return result

    def create_thirdparties_notifications_for_tid(self, objid, thirdpartiesCreateCompanyNotificationModel):
        """
        @endpoint 'post /thirdparties/{id}/notifications'
        Create thirdparty notifications on thirdparty id
        @id     int     ID of thirdparty
        @thirdpartiesCreateCompanyNotificationModel     str     { request_data (Array[string], optional): Request data }
        @return: json with new thirdparty notification
        """
        action = 'notifications'
        result = self.call_action_api('thirdparties', objid, action, params=thirdpartiesCreateCompanyNotificationModel)
        return result
        # Example thirdpartiesCreateCompanyNotificationModel contents { "event": "114", "socid": "5", "contact_id": "8", "type": "email" }

    def delete_thirdparties_notifications_for_tid(self, objid, notid):
        """
        @endpoint 'delete /thirdparties/{id}/notifications/{notification_id}'
        Delete thirdparty notifications based on thirdparty id and notification id
        @id               int     ID of thirdparty
        @notification_id  int     ID of CompanyNotification
        @return: 1 and response code 200 if successful. 403 if notification id does not exist
        """
        if self.debug:
            ic()
            ic(objid)
            ic(notid)
        objstr = str(objid) + '/notifications/' + str(notid)
        result = self.call_delete_api('thirdparties', objstr)
        return result

    # update does not seem to work with dolibarr v20.0.0
    def update_thirdparties_notifications_for_tid(self, objid, notid=None, thirdpartiesUpdateCompanyNotificationModel={}):
        """
        @endpoint 'put /thirdparties/{id}/notifications/{notification_id}'
        Update CompanyNotification object for thirdparty
        @id               int     ID of thirdparty
        @notification_id  int     ID of CompanyNotification
        @thirdpartiesUpdateCompanyNotificationModel     str     { request_data (Array[string], optional): Request data }
        @return: json with updated thirdparty notification
        """
        if self.debug:
            ic()
            ic(objid)
            ic(notid)
            ic(thirdpartiesUpdateCompanyNotificationModel)
        objstr = str(objid) + '/notifications' + str(notid)
        result = self.call_update_api('thirdparties', objid, thirdpartiesUpdateCompanyNotificationModel, extra_object='notifications', extra_id=notid )
        return result
        # Example thirdpartiesUpdateCompanyNotificationModel contents { "event": "114", "socid": "5", "contact_id": "8", "type": "email" }

    def get_thirdparties_outstanding_by_tid(self, objid, otype, mode):
        """
        @endpoint 'get /thirdparties/{id}/outstandinginvoices'
        @endpoint 'get /thirdparties/{id}/outstandingorders'
        @endpoint 'get /thirdparties/{id}/outstandingproposals'
        Get thirdparty outstanding <otype> based on thirdparty id, otype and mode
        @otype string 'invoices', 'orders' or 'proposals' 
        @mode string 'customer' or 'supplier'
        @return: list of thirdparty's <otype> invoices
        """
        if mode:
            objid = str(objid) + '/outstanding' + otype + '?mode=' + mode
        else:
            objid = str(objid) + '/outstanding' + otype
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_representatives_by_tid(self, objid, mode):
        """
        @endpoint 'get /thirdparties/{id}/representatives'
        Get thirdparty representatives based on thirdparty id and mode
        @mode string 0=Array with properties, 1=Array of id.
        @return: list of thirdparty's representatives
        """
        if mode:
            objid = str(objid) + '/representatives?mode=' + mode
        else:
            objid = str(objid) + '/representatives'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_accounts_by_tid(self, objid, site):
        """
        @endpoint 'get /thirdparties/{id}/accounts'
        Get thirdparty accounts based on thirdparty id and site
        @mode string 0=Array with properties, 1=Array of id.
        @return: list of thirdparty's accounts
        """
        if site:
            objid = str(objid) + '/accounts?site=' + site
        else:
            objid = str(objid) + '/accounts'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_all_thirdparties_categories_by_tid(self, objid, from_ThirdpartyFilter = None, mode = 'customer'):
        """
        @endpoint 'get /thirdparties/{id}/categories'
        @endpoint 'get /thirdparties/{id}/supplier_categories'
        Get all categories for a thirdparties based on it's thirdparty_id
        @param from_ThirdpartyFilter:
        @mode string 'customer' or 'supplier'
        @return: list of a thirdpartiess categories
        """
        if self.debug:
            ic()
            ic(from_ThirdpartyFilter)
        if from_ThirdpartyFilter is None:
            search_filter = ThirdpartyFilter()
        else:
            search_filter = from_ThirdpartyFilter
        all_thirdparties_categories=[]
        page = 0
        while True:
            some_thirdparties_categories = self.get_some_thirdparties_categories_by_tid(objid, search_filter, mode, page)
            if self.debug:
                ic(some_thirdparties_categories)
            if "error" in some_thirdparties_categories:
                break
            elif [] == some_thirdparties_categories:
                break
            elif {} == some_thirdparties_categories:
                break
            else:
                page += 1
                if some_thirdparties_categories == all_thirdparties_categories:
                    break
                all_thirdparties_categories = all_thirdparties_categories + list(some_thirdparties_categories)
        return all_thirdparties_categories

    def get_some_thirdparties_categories_by_tid(self, objid, from_ThirdpartyFilter = None, mode = 'customer', page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ThirdpartyFilter)
        if from_ThirdpartyFilter is None:
            search_filter = ThirdpartyFilter()
        else:
            search_filter = from_ThirdpartyFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        category = params.get("category")
        if category:
            raise Exception("sorry, you can not use category in this filter, try without")
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        properties = params.get("properties")
        if properties:
            raise Exception("sorry, you can not use properties in this filter, try without")
        sqlfilters = params.get("sqlfilters")
        if sqlfilters:
            raise Exception("sorry, you can not use sqlfilters in this filter, try without")
        typeid = params.get("typeid")
        if typeid:
            raise Exception("sorry, you can not use typeid in this filter, try without")
        if 'supplier' == mode:
            api_path = 'thirdparties/' + str(objid) + '/supplier_categories'
        else:
            # assuming that they ask for customer
            api_path = 'thirdparties/' + str(objid) + '/categories'
        result = self.call_list_api(api_path, params)
        return result

    def get_thirdparties_fixedamountdiscounts_by_tid(self, objid, filter):
        """
        @endpoint 'get /thirdparties/{id}/fixedamountdiscounts'
        Get thirdparty fixedamountdiscounts based on thirdparty id and filter
        @filter Filter exceptional discount. "none" will return every discount, "available" returns unapplied discounts, "used" returns applied discounts
        @return: list of thirdparty's fixedamountdiscounts
        """
        if filter:
            objid = str(objid) + '/fixedamountdiscounts?filter=' + filter
        else:
            objid = str(objid) + '/fixedamountdiscounts'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_generateBankAccountDocument_by_tid(self, objid, companybankid, model = 'sepamandate'):
        """
        @endpoint 'get /thirdparties/{id}/generateBankAccountDocument/{companybankid}/{model}'
        Get thirdparty generateBankAccountDocument based on thirdparty id, companybankid and model
        @companybankid
        @model default is 'sepamandate'
        @return: list of thirdparty's accounts
        """
        objid = str(objid) + '/generateBankAccountDocument/' + str(companybankid) + '/' + str(model)
        result = self.call_get_api('thirdparties', objid)
        return result

    def update_thirdparty_by_tid(self, objid, updateThirdpartiesModel):
        """
        @endpoint 'put /thirdparties/{id}'
        Update thirdparty
        @modulepart     str     Name of module or area concerned by file download ('product', ...)
        @id int Id of thirdparty to update
        @updateThirdpartiesModel     str     updateThirdpartiesModel {request_data (Array[string], optional): Datas }
        @return: thirdparty
        """
        if self.debug:
            ic()
            ic(objid)
            ic(updateThirdpartiesModel)
        result = self.call_update_api('thirdparties', objid,updateThirdpartiesModel )
        return result

    # CONTACTS
    def find_all_contacts(self, from_ContactFilter = None):
        """
        @endpoint 'get /contacts'
        Get all contacts
        @param from_ContactFilter:
        @return: list of a contacts
        """
        if self.debug:
            ic()
            ic(from_ContactFilter)
        if from_ContactFilter is None:
            search_filter = ContactFilter()
        else:
            search_filter = from_ContactFilter
        all_contacts=[]
        page = 0
        while True:
            some_contacts = self.find_some_contacts(search_filter, page)
            if "error" in some_contacts:
                break
            elif [] == some_contacts:
                break
            elif {} == some_contacts:
                break
            else:
                page += 1
                if some_contacts == all_contacts:
                    break
                all_contacts = all_contacts + list(some_contacts)
        return all_contacts

    def find_some_contacts(self, from_ContactFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ContactFilter)
        if from_ContactFilter is None:
            search_filter = ContactFilter()
        else:
            search_filter = from_ContactFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('contacts', params)
        return result

    def get_contact_by_cid(self, objid, includecount = 0, includeroles = 0):
        """
        @endpoint 'get /contacts/{id}'
        Get contact based on contact id
        @includecount Count and return also number of elements the contact is used as a link for
        @includeroles Includes roles of the contact
        @return: contact
        """
        objid = str(objid) + '?includecount=' + str(includecount) + '&includeroles=' + str(includeroles)
        result = self.call_get_api('contacts', objid=objid)
        return result

    def get_contact_by_email(self, email, includecount = 0, includeroles = 0):
        """
        @endpoint 'get /contacts/email/{email}'
        Get contact based on contact email
        @includecount Count and return also number of elements the contact is used as a link for
        @includeroles Includes roles of the contact
        @return: contact
        """
        email = urllib.parse.quote(email) + '?includecount=' + str(includecount) + '&includeroles=' + str(includeroles)
        result = self.call_get_api('contacts/email', email)
        return result

    def get_all_contacts_categories_by_cid(self, objid, from_ContactFilter = None):
        """
        @endpoint 'get /contacts/{id}/categories'
        Get all categories for a contact based on it's contact_id
        @param from_ContactFilter:
        @return: list of a contacts categories
        """
        if self.debug:
            ic()
            ic(from_ContactFilter)
        if from_ContactFilter is None:
            search_filter = ContactFilter()
        else:
            search_filter = from_ContactFilter
        all_contacts_categories=[]
        page = 0
        while True:
            some_contacts_categories = self.get_some_contacts_categories_by_cid(objid, search_filter, page)
            if self.debug:
                ic(some_contacts_categories)
            if 0 == some_contacts_categories:
                break
            elif [] == some_contacts_categories:
                break
            elif {} == some_contacts_categories:
                break
            elif "error" in some_contacts_categories:
                break
            else:
                page += 1
                if some_contacts_categories == all_contacts_categories:
                    break
                all_contacts_categories = all_contacts_categories + list(some_contacts_categories)
        return all_contacts_categories

    def get_some_contacts_categories_by_cid(self, objid, from_ContactFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ContactFilter)
        if from_ContactFilter is None:
            search_filter = ContactFilter()
        else:
            search_filter = from_ContactFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        category = params.get("category")
        if category:
            raise Exception("sorry, you can not use category in this filter, try without")
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        properties = params.get("properties")
        if properties:
            raise Exception("sorry, you can not use properties in this filter, try without")
        sqlfilters = params.get("sqlfilters")
        if sqlfilters:
            raise Exception("sorry, you can not use sqlfilters in this filter, try without")
        typeid = params.get("typeid")
        if typeid:
            raise Exception("sorry, you can not use typeid in this filter, try without")
        api_path = 'contacts/' + str(objid) + '/categories'
        result = self.call_list_api(api_path, params)
        return result

    def update_contact_by_cid(self, objid, updateContactModel):
        """
        @endpoint 'put /contacts/{id}'
        Update contact
        @id int Id of contact to update
        @updateContactModel     str     updateContactModel {request_data (Array[string], optional): Datas }
        @return: contact
        """
        if self.debug:
            ic()
            ic(objid)
            ic(updateContactModel)
        result = self.call_update_api('contacts', objid,updateContactModel )
        return result

    # SUBSCRIPTIONS
    def find_all_subscriptions(self, from_SubscriptionFilter = None):
        """
        @endpoint 'get /subscriptions'
        Get all subscriptions
        @param from_SubscriptionFilter:
        @return: list of a subscriptions
        """
        if self.debug:
            ic()
            ic(from_SubscriptionFilter)
        if from_SubscriptionFilter is None:
            search_filter = SubscriptionFilter()
        else:
            search_filter = from_SubscriptionFilter
        all_subscriptions=[]
        page = 0
        while True:
            some_subscriptions = self.find_some_subscriptions(search_filter, page)
            if "error" in some_subscriptions:
                break
            elif [] == some_subscriptions:
                break
            elif {} == some_subscriptions:
                break
            else:
                page += 1
                if some_subscriptions == all_subscriptions:
                    break
                all_subscriptions = all_subscriptions + list(some_subscriptions)
        return all_subscriptions

    def find_some_subscriptions(self, from_SubscriptionFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_SubscriptionFilter)
        if from_SubscriptionFilter is None:
            search_filter = SubscriptionFilter()
        else:
            search_filter = from_SubscriptionFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('subscriptions', params)
        return result

    def get_subscription_by_sid(self, objid):
        """
        @endpoint 'get /subscriptions/{id}'
        Get subscription based on subscription id
        @return: subscription
        """
        result = self.call_get_api('subscriptions', objid=objid)
        return result

    # PROPOSALS
    def find_all_proposals(self, from_ProposalFilter = None):
        """
        @endpoint 'get /proposals'
        Get all proposals
        @param from_ProposalFilter:
        @return: list of a proposals
        """
        if self.debug:
            ic()
            ic(from_ProposalFilter)
        if from_ProposalFilter is None:
            search_filter = ProposalFilter()
        else:
            search_filter = from_ProposalFilter
        all_proposals=[]
        page = 0
        while True:
            some_proposals = self.find_some_proposals(search_filter, page)
            if "error" in some_proposals:
                break
            elif [] == some_proposals:
                break
            elif {} == some_proposals:
                break
            else:
                page += 1
                if some_proposals == all_proposals:
                    break
                all_proposals = all_proposals + list(some_proposals)
        return all_proposals

    def find_some_proposals(self, from_ProposalFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_ProposalFilter)
        if from_ProposalFilter is None:
            search_filter = ProposalFilter()
        else:
            search_filter = from_ProposalFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('proposals', params)
        return result

    def get_proposal_by_pid(self, objid, contact_list = 1):
        """
        @endpoint 'get /proposals/{id}'
        Get proposal based on proposal id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: proposal
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('proposals', objid=objid)
        return result

    def update_proposal_with_pid(self, objid, updateProposalsModel):
        """
        @endpoint 'put /proposals/{id}'
        Update proposal
        @id     int     Id of proposal to update
        @updateProposalsModel     str     updateProposalsModel {request_data (Array[string], optional): Datas }
        @return: proposal
        """
        if self.debug:
            ic()
            ic(objid)
            ic(updateProposalsModel)
        result = self.call_update_api('proposals', objid,updateProposalsModel )
        return result

    def update_proposal_line_with_lineid(self, pid, lineid, updateProposalLineModel):
        """
        @endpoint 'put /proposals/{id}/lines({lineid})'
        Update proposal
        @pid     int     Id of proposal with line to update
        @lineid     int     Id of line to update
        @updateProposalLineModel     str     updateProposalLineModel {request_data (Array[string], optional): Datas }
        @return: proposal
        """
        if self.debug:
            ic()
            ic(pid)
            ic(lineid)
            ic(updateProposalLineModel)
        result = self.call_update_api('proposals', pid, updateProposalLineModel, "lines", lineid)
        return result

    def get_proposal_by_ref(self, objref, contact_list = 1):
        """
        @endpoint 'get /proposals/ref/{ref}'
        Get proposal based on proposal ref
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: proposal
        """
        objref = 'ref/' + urllib.parse.quote(objref) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('proposals', objid=objref)
        return result

    # 2024-04-22 doesn't work for me in my Dolibarr
    def get_proposal_by_ref_ext(self, objref_ext, contact_list = 1):
        """
        @endpoint 'get /proposals/ref_ext/{ref_ext}'
        Get proposal based on proposal ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: proposal
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('proposals', objid=objref_ext)
        return result

    def get_proposal_lines_by_pid(self, objid, sqlfilters):
        """
        @endpoint 'get /proposals/{id}/lines'
        Get proposal lines based on proposal id
        @sqlfilters string Other criteria to filter answers separated by a comma. d is the alias for proposal lines table, p is the alias for product table. "Syntax example "(p.ref:like:'SO-%') AND (d.date_start:
        @return: proposal lines
        """
        objid = str(objid) + '/lines?sqlfilters=' + str(sqlfilters)
        result = self.call_get_api('proposals', objid=objid)
        return result

    def close_proposal_by_pid(self, objid, proposalsCloseModel):
        """
        @endpoint 'post /proposals/{id}/close'
        Close (Accept or refuse) a quote / commercial proposal
        @return: proposal
        """
        if self.debug:
            ic()
            ic(objid)
            ic(proposalsCloseModel)
        objid = str(objid)
        trigger_defined = proposalsCloseModel.get('notrigger')
        if trigger_defined is None:
            proposalsCloseModel['notrigger'] = 0

        result = self.call_action_api('proposals', objid=objid, action='close', params=proposalsCloseModel)
        return result

    def proposal_rejected(self, objid, note_private = "", note_public=""):
        if self.debug:
            ic()
            ic(objid)
            ic(note_private)
            ic(note_public)
        params = {
            "status": 3,
            "note_private": note_private,
            "note_public": note_public
        }
        result = self.close_proposal_by_pid(objid=objid, proposalsCloseModel=params)
        return result

    def proposal_accepted(self, objid, note_private = "", note_public=""):
        params = {
            "status": 2,
            "note_private": note_private,
            "note_public": note_public
        }
        result = self.close_proposal_by_pid(objid=objid, proposalsCloseModel=params)
        return result

    def validate_proposal_by_pid(self, objid, notrigger = 0):
        """
        @endpoint 'post /proposals/{id}/validate'
        Validate a commercial proposal
        @return: proposal
        """
        if self.debug:
            ic()
            ic(objid)
            ic(notrigger)
        objid = str(objid)
        proposalsValidateModel = {
            "notrigger": notrigger
        }
        result = self.call_action_api('proposals', objid=objid, action='validate', params=proposalsValidateModel)
        return result

    def proposal_add_contact(self, objid, contactid, type, source = None):
        """
        @endpoint 'post /proposals/{id}/contact/{contactid}/{type}
        Add a contact type of given commercial proposal
        @id         int     Id of commercial proposal to update
        @contactid  int     Id of contact to add
        @type       str     Type of the contact (BILLING, SHIPPING, CUSTOMER)
        @source     str     Source of the contact (internal, external)
        @return:    array   JSON with result
        """
        if self.debug:
            ic()
            ic(objid)
            ic(contactid)
            ic(type)
        if source:
            action = "contact/" + str(contactid) + "/" + str(type) + "/" + str(source)
        else:
            action = "contact/" + str(contactid) + "/" + str(type) + "/external"
        result = self.call_action_api('proposals', objid=objid, action=action)
        return result

    # ORDERS
    def find_all_orders(self, from_OrderFilter = None):
        """
        @endpoint 'get /orders'
        Get all orders
        @param from_OrderFilter:
        @return: list of a orders
        """
        if self.debug:
            ic()
            ic(from_OrderFilter)
        if from_OrderFilter is None:
            search_filter = OrderFilter()
        else:
            search_filter = from_OrderFilter
        all_orders=[]
        page = 0
        while True:
            some_orders = self.find_some_orders(search_filter, page)
            if "error" in some_orders:
                break
            elif [] == some_orders:
                break
            elif {} == some_orders:
                break
            else:
                page += 1
                if some_orders == all_orders:
                    break
                all_orders = all_orders + list(some_orders)
        return all_orders

    def find_some_orders(self, from_OrderFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_OrderFilter)
        if from_OrderFilter is None:
            search_filter = OrderFilter()
        else:
            search_filter = from_OrderFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('orders', params)
        return result

    def get_order_by_oid(self, objid, contact_list = 1):
        """
        @endpoint 'get /orders/{id}'
        Get order based on order id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: order
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('orders', objid=objid)
        return result

    def update_order_with_oid(self, objid, updateOrdersModel):
        """
        @endpoint 'put /orders/{id}'
        Update order
        @id     int     Id of order to update
        @updateOrdersModel     str     updateOrdersModel {request_data (Array[string], optional): Datas }
        @return: order
        """
        if self.debug:
            ic()
            ic(objid)
            ic(updateOrdersModel)
        result = self.call_update_api('orders', objid,updateOrdersModel )
        return result

    def get_order_contacts_by_oid(self, objid, ctype = ''):
        """
        @endpoint 'get /orders/{id}/contacts'
        Get order based on order id and contact type
        @ctype string Type of the contact (BILLING, SHIPPING, CUSTOMER)
        @return: order
        """
        objid = str(objid) + '/contacts?type=' + str(ctype)
        result = self.call_get_api('orders', objid=objid)
        return result

    def get_order_by_ref(self, objref, contact_list = 1):
        """
        @endpoint 'get /orders/ref/{ref}'
        Get order based on order ref
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: order
        """
        objref = 'ref/' + urllib.parse.quote(objref) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('orders', objid=objref)
        return result

    # 2024-04-22 doesn't work for me in my Dolibarr
    def get_order_by_ref_ext(self, objref_ext, contact_list = 1):
        """
        @endpoint 'get /orders/ref_ext/{ref_ext}'
        Get order based on order ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: order
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('orders', objid=objref_ext)
        return result

    def get_order_lines_by_oid(self, objid):
        """
        @endpoint 'get /orders/{id}/lines'
        Get order lines based on order id
        @return: order lines
        """
        objid = str(objid) + '/lines'
        result = self.call_get_api('orders', objid=objid)
        return result

    def get_order_shipment_by_oid(self, objid):
        """
        @endpoint 'get /orders/{id}/shipment'
        Get order shipment based on order id
        @return: order shipment
        """
        objid = str(objid) + '/shipment'
        result = self.call_get_api('orders', objid=objid)
        return result

    def delete_order_by_oid(self, objid):
        """
        @endpoint 'put /orders/{id}'
        Cancel an order
        @return: order
        """
        if self.debug:
            ic()
            ic(objid)

        result = self.call_delete_api('orders', objid=objid)
        return result

    # INVOICES
    def find_all_invoices(self, from_InvoiceFilter = None):
        """
        @endpoint 'get /invoices'
        Get all invoices
        @param from_InvoiceFilter:
        @return: list of a invoices
        """
        if self.debug:
            ic()
            ic(from_InvoiceFilter)
        if from_InvoiceFilter is None:
            search_filter = InvoiceFilter()
        else:
            search_filter = from_InvoiceFilter
        all_invoices=[]
        page = 0
        while True:
            some_invoices = self.find_some_invoices(search_filter, page)
            if "error" in some_invoices:
                break
            elif [] == some_invoices:
                break
            elif {} == some_invoices:
                break
            else:
                page += 1
                if some_invoices == all_invoices:
                    break
                all_invoices = all_invoices + list(some_invoices)
        return all_invoices

    def find_some_invoices(self, from_InvoiceFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_InvoiceFilter)
        if from_InvoiceFilter is None:
            search_filter = InvoiceFilter()
        else:
            search_filter = from_InvoiceFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('invoices', params)
        return result

    def get_invoice_by_iid(self, objid, contact_list = 1):
        """
        @endpoint 'get /invoices/{id}'
        Get invoice based on invoice id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objid)
        return result

    def update_invoice_with_iid(self, objid, updateInvoicesModel):
        """
        @endpoint 'put /invoices/{id}'
        Update invoice
        @id     int     Id of invoice to update
        @updateInvoicesModel     str     updateInvoicesModel {request_data (Array[string], optional): Datas }
        @return: invoice
        """
        if self.debug:
            ic()
            ic(objid)
            ic(updateInvoicesModel)
        result = self.call_update_api('invoices', objid, updateInvoicesModel )
        return result

    def get_invoice_discounts_by_iid(self, objid):
        """
        @endpoint 'get /invoices/{id}/discount'
        Get invoice discounts based on invoice id
        @return: discount
        """
        objid = str(objid) + '/discount'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_by_ref(self, objref, contact_list = 1):
        """
        @endpoint 'get /invoices/ref/{ref}'
        Get invoice based on invoice ref
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice
        """
        objref = 'ref/' + urllib.parse.quote(objref) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objref)
        return result

    # 2024-04-22 doesn't work for me in my Dolibarr
    def get_invoice_by_ref_ext(self, objref_ext, contact_list = 1):
        """
        @endpoint 'get /invoices/ref_ext/{ref_ext}'
        Get invoice based on invoice ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objref_ext)
        return result

    def get_invoice_lines_by_iid(self, objid):
        """
        @endpoint 'get /invoices/{id}/lines'
        Get invoice lines based on invoice id
        @return: invoice lines
        """
        objid = str(objid) + '/lines'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_payments_by_iid(self, objid):
        """
        @endpoint 'get /invoices/{id}/payments'
        Get invoice payments based on invoice id
        @return: invoice payments
        """
        objid = str(objid) + '/payments'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_template_by_tid(self, objid, contact_list = 1):
        """
        @endpoint 'get /invoices/templates/{id}'
        Get invoice payments based on invoice template id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice payments
        """
        objid = 'payments/' + str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objid)
        return result


    # INTERVENTIONS
    def find_all_interventions(self, from_InterventionFilter = None):
        """
        @endpoint 'get /interventions'
        Get all interventions
        @param from_InterventionFilter:
        @return: list of a interventions
        """
        if self.debug:
            ic()
            ic(from_InterventionFilter)
        if from_InterventionFilter is None:
            search_filter = InterventionFilter()
        else:
            search_filter = from_InterventionFilter
        all_interventions=[]
        page = 0
        while True:
            some_interventions = self.find_some_interventions(search_filter, page)
            if "error" in some_interventions:
                break
            elif [] == some_interventions:
                break
            elif {} == some_interventions:
                break
            else:
                page += 1
                if some_interventions == all_interventions:
                    break
                all_interventions = all_interventions + list(some_interventions)
        return all_interventions

    def find_some_interventions(self, from_InterventionFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_InterventionFilter)
        if from_InterventionFilter is None:
            search_filter = InterventionFilter()
        else:
            search_filter = from_InterventionFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('interventions', params)
        return result

    def get_intervention_by_iid(self, objid):
        """
        @endpoint 'get /interventions/{id}'
        Get intervention based on intervention id
        @return: invoice
        """
        objid = str(objid)
        result = self.call_get_api('interventions', objid=objid)
        return result


    # TICKETS
    def find_all_tickets(self, from_TicketFilter = None):
        """
        @endpoint 'get /tickets'
        Get all tickets
        @param from_TicketFilter:
        @return: list of a tickets
        """
        if self.debug:
            ic()
            ic(from_TicketFilter)
        if from_TicketFilter is None:
            search_filter = TicketFilter()
        else:
            search_filter = from_TicketFilter
        all_tickets=[]
        page = 0
        while True:
            some_tickets = self.find_some_tickets(search_filter, page)
            if "error" in some_tickets:
                break
            elif [] == some_tickets:
                break
            elif {} == some_tickets:
                break
            else:
                page += 1
                if some_tickets == all_tickets:
                    break
                all_tickets = all_tickets + list(some_tickets)
        return all_tickets

    def find_some_tickets(self, from_TicketFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_TicketFilter)
        if from_TicketFilter is None:
            search_filter = TicketFilter()
        else:
            search_filter = from_TicketFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('tickets', params)
        return result

    def get_ticket_by_iid(self, objid):
        """
        @endpoint 'get /tickets/{id}'
        Get ticket based on ticket id
        @return: ticket
        """
        objid = str(objid)
        result = self.call_get_api('tickets', objid=objid)
        return result

    def get_ticket_by_ref(self, objref):
        """
        @endpoint 'get /tickets/ref/{ref}'
        Get ticket based on ticket ref
        @return: ticket
        """
        objref = 'ref/' + str(objref)
        result = self.call_get_api('tickets', objid=objref)
        return result

    def get_ticket_by_track_id(self, objtrack_id):
        """
        @endpoint 'get /tickets/track_id/{track_id}'
        Get ticket based on ticket track_id
        @return: ticket
        """
        objtrack_id = 'track_id/' + str(objtrack_id)
        result = self.call_get_api('tickets', objid=objtrack_id)
        return result


    # USERS
    def find_all_users(self, from_UserFilter = None):
        """
        @endpoint 'get /users'
        Get all users
        @param from_UserFilter:
        @return: list of a users
        """
        if self.debug:
            ic()
            ic(from_UserFilter)
        if from_UserFilter is None:
            search_filter = UserFilter()
        else:
            search_filter = from_UserFilter
        all_users=[]
        page = 0
        while True:
            some_users = self.find_some_users(search_filter, page)
            if "error" in some_users:
                break
            elif [] == some_users:
                break
            elif {} == some_users:
                break
            else:
                page += 1
                if some_users == all_users:
                    break
                all_users = all_users + list(some_users)
        return all_users

    def find_some_users(self, from_UserFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_UserFilter)
        if from_UserFilter is None:
            search_filter = UserFilter()
        else:
            search_filter = from_UserFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('users', params)
        return result

    def get_user_by_uid(self, objid, includepermissions = 0):
        """
        @endpoint 'get /users/{id}'
        Get user based on user id
        @includepermissions int default 0, Set this to 1 to have the array of permissions loaded (not done by default for performance purpose)
        @return: user
        """
        if includepermissions:
            objid = str(objid)  + '?includepermissions=' + includepermissions
        else:
            objid = str(objid)
        result = self.call_get_api('users', objid=objid)
        return result

    def get_user_groups_uid(self, objid):
        """
        @endpoint 'get /users/{id}/groups'
        Get user groups based on user id
        @return: list of user groups
        """
        objid = str(objid) + '/groups'
        result = self.call_get_api('users', objid)
        return result

    def setgroup_user_uid(self, objid, groupid, entity = 1):
        """
        @endpoint 'get /users/{id}/setGroup/{group}'
        Set group for user based on user and group id
        @groupid int Group ID
        @entity int Entity ID (valid only for superadmin in multicompany transverse mode) default = 1
        @return: int
        """
        objid = str(objid) + '/setGroup/' + str(groupid) + '?entity=' + str(entity)
        result = self.call_get_api('users', objid)
        return result

    def get_user_by_email(self, email, includepermissions = 0):
        """
        @endpoint 'get /users/email/{email}'
        Get properties of an user object by Email
        @return: user object
        """
        if includepermissions:
            objid = 'email/' + urllib.parse.quote(email)  + '?includepermissions=' + includepermissions
        else:
            objid = str(objid)
        result = self.call_get_api('users', objid=objid)
        return result

    # STATUS
    def get_status(self):
        """
        @endpoint 'get /status'
        Get status info from /status
        @return: status information
        """

        result = self.call_get_api('status', '')
        return result

    # SETUP
    def get_setup_company(self):
        """
        @endpoint 'get /setup/company'
        Get company info from /setup
        @return: Company information
        """

        result = self.call_get_api('setup', 'company')
        return result

    def get_setup_conf(self, constantname):
        """
        @endpoint 'get /setup/conf/{constantname}'
        Get conf info from /setup - Note that conf variables that stores security key or password hashes can't be loaded with API.
        @return: Configuration information
        """

        result = self.call_get_api('setup/conf', constantname)
        return result

    def get_setup_extrafields(self):
        """
        @endpoint 'get /setup/extrafields'
        Get extrafields info from /setup
        @return: extrafields information
        """

        result = self.call_get_api('setup', 'extrafields')
        return result

    def get_setup_modules(self):
        """
        @endpoint 'get /setup/modules'
        Get modules info from /setup
        @return: modules information
        """

        result = self.call_get_api('setup', 'modules')
        return result

    # SETUP / DICTIONARIES
    def get_setup_dictionary_currencies(self):
        """
        @endpoint 'get /setup/dictionary/currencies'
        Get currencies info from /setup/dictionary
        @return: currencies information
        """

        result = self.call_get_api('setup', 'dictionary/currencies')
        return result

    def find_all_countries(self, from_countryFilter = None):
        """
        @endpoint 'get /setup/dictionary/countries'
        Get all countries
        @param from_countryFilter:
        @return: list of a countries
        """
        if self.debug:
            ic()
            ic(from_countryFilter)
        if from_countryFilter is None:
            search_filter = countryFilter()
        else:
            search_filter = from_countryFilter
        all_countries=[]
        page = 0
        while True:
            some_countries = self.find_some_countries(search_filter, page)
            if "error" in some_countries:
                break
            elif [] == some_countries:
                break
            elif {} == some_countries:
                break
            else:
                page += 1
                if some_countries == all_countries:
                    break
                all_countries = all_countries + list(some_countries)
        return all_countries

    def find_some_countries(self, from_countryFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_countryFilter)
        if from_countryFilter is None:
            search_filter = countryFilter()
        else:
            search_filter = from_countryFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('setup/dictionary/countries', params)
        return result

    def get_country_by_code(self, country_code):
        """
        @endpoint 'get /setup/dictionary/countries/byCode/{code}'
        """
        result = self.call_get_api('setup/dictionary/countries/byCode', objid=country_code)
        return result

    def find_all_states(self, from_stateFilter = None):
        """
        @endpoint 'get /setup/dictionary/states'
        Get all states
        @param from_stateFilter:
        @return: list of a states
        """
        if self.debug:
            ic()
            ic(from_stateFilter)
        if from_stateFilter is None:
            search_filter = stateFilter()
        else:
            search_filter = from_stateFilter
        all_states=[]
        page = 0
        while True:
            some_states = self.find_some_states(search_filter, page)
            if "error" in some_states:
                break
            elif [] == some_states:
                break
            elif {} == some_states:
                break
            else:
                page += 1
                if some_states == all_states:
                    break
                all_states = all_states + list(some_states)
        return all_states

    def find_some_states(self, from_stateFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_stateFilter)
        if from_stateFilter is None:
            search_filter = stateFilter()
        else:
            search_filter = from_stateFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('setup/dictionary/states', params)
        return result

    def get_state_by_code(self, state_code):
        """
        @endpoint 'get /setup/dictionary/states/byCode/{code}'
        """
        result = self.call_get_api('setup/dictionary/states/byCode', objid=state_code)
        return result


    # CATEGORIES
    def find_all_categories(self, from_categoryFilter = None):
        """
        @endpoint 'get /categories'
        Get all categories
        @param from_categoryFilter:
        @return: list of a categories
        """
        if self.debug:
            ic()
            ic(from_categoryFilter)
        if from_categoryFilter is None:
            search_filter = CategoryFilter()
        else:
            search_filter = from_categoryFilter
        all_categories=[]
        page = 0
        while True:
            some_categories = self.find_some_categories(search_filter, page)
            if "error" in some_categories:
                break
            elif [] == some_categories:
                break
            elif {} == some_categories:
                break
            else:
                page += 1
                if some_categories == all_categories:
                    break
                all_categories = all_categories + list(some_categories)
        return all_categories

    def find_some_categories(self, from_categoryFilter = None, page = 0):
        if self.debug:
            ic()
            ic(page)
            ic(from_categoryFilter)
        if from_categoryFilter is None:
            search_filter = CategoryFilter()
        else:
            search_filter = from_categoryFilter
        search_filter = replace(search_filter, page=page)
        params = asdict(search_filter)
        result = self.call_list_api('categories', params)
        return result

    def get_category_by_id(self, catid, include_childs=False):
        """
        @endpoint 'get /categories/{id}'
        """
        if include_childs:
            catid = str(catid) + '?include_childs=true'
        else:
            catid = str(catid) + '?include_childs=false'
        result = self.call_get_api('categories', objid=catid)
        return result

    # DOCUMENTS
    def get_documents(self, modulepart, id = '', ref = '', sortfield = 'date', sortorder = 'asc'):
        """
        @endpoint 'get /documents'
        Return the list of documents of a dedicated element (from its ID or Ref)
        @modulepart str Name of module or area concerned ('thirdparty', 'member', 'proposal', 'order', 'invoice', 'supplier_invoice', 'shipment', 'project', ...)
        @id int         ID of element
        @ref str        REF of element
        @sortfield str  Sort criteria ('','fullname','relativename','name','date','size')
        @sortorder str  Sort order ('asc' or 'desc')
        @return: list of a documents
        """
        document_choices = "documents?"
        if '' != modulepart:
            document_choices = document_choices + 'modulepart=' + str(modulepart) + '&'
        if '' != str(id):
            document_choices = document_choices + 'id=' + str(id) + '&'
        if '' != ref:
            document_choices = document_choices + 'ref=' + ref + '&'
        if '' != sortfield:
            document_choices = document_choices + 'sortfield=' + sortfield + '&'
        if '' != sortorder:
            document_choices = document_choices + 'sortorder=' + sortorder

        result = self.call_list_api(document_choices, {})
        if "error" in result:
            ic(result)
            return []
        return result

    def delete_documents(self, modulepart, original_file = '', document_dict = {}):
        """
        @endpoint 'delete /documents'
        Delete a document.
        @modulepart     str     Name of module or area concerned by file download ('product', ...)
        @original_file  str     Relative path with filename, relative to modulepart (for example: PRODUCT-REF-999/IMAGE-999.jpg)
        @return: json with success or error
        """
        if '' == original_file and document_dict is not None:
            level1name = document_dict.get("level1name")
            relativename = document_dict.get("relativename")
            if level1name and relativename:
                original_file = str(level1name) + "/" + str(relativename)
        else:
            error = "Come on, give me at least 1 non empty variable"
            ic(error)

        combined_url = 'documents?modulepart=' + str(modulepart) + '&original_file=' + str(original_file)
        result = self.call_delete_api('', combined_url)
        if "error" in result:
            ic(result)
        return result

    def build_document_by_ref(self, modulepart, objref, documentsBuilddocModel = {}):
        """
        @endpoint 'put /documents/builddoc'
        Build documents
        @modulepart     str     Name of module or area concerned by file download ('product', ...)
        @objref         str     The reference of the object we want a document for
        @documentsBuilddocModel json    { modulepart, original_file, doctemplate, langcode }
        @original_file  str     Relative path with filename, relative to modulepart (for example: IN201701-999/IN201701-999.pdf).
        @doctemplate    str     (optional) Set here the doc template to use for document generation (If not set, use the default template).
        @langcode       str     (optional) Language code like 'en_US', 'fr_FR', 'es_ES', ... (If not set, use the default language).
        @return: thirdparty
        """
        if self.debug:
            ic()
            ic(modulepart)
            ic(objref)
            ic(documentsBuilddocModel)

        if "proposal" == modulepart:
            modulepart = "propal"
        documentsBuilddocModel["modulepart"]    = modulepart
        documentsBuilddocModel["original_file"] = str(objref + "/" + objref + ".pdf")
        result = self.call_update_api(object='documents/builddoc', objid=None, params=documentsBuilddocModel)
        return result
