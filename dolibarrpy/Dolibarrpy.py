import requests
import logging
import json, urllib
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

@dataclass
class MemberFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    typeid: Optional[str] = None        # only get members with this thirdparty_id
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
    category: Optional[int] = None      # only get members with this status: draft | unpaid | paid | cancelled
    sqlfilters: Optional[str] = None    # (t.email:like:'john.doe@example.com')
    properties: Optional[str] = None    # Restrict the data returned to these properties. Ignored if empty. Comma separated list of properties names

@dataclass
class ContactFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None          # page number
    thirdparty_ids: Optional[str] = None    # Thirdparty ids to filter contacts of (example '1' or '1,2,3')
    category: Optional[int] = None      # only get members with this status: draft | unpaid | paid | cancelled
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
class ProposalFilter():
    sortfield: Optional[str] = None
    sortorder: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    # Syntax example "(t.statut:=:1)
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
    def find_all_shipments(self, from_ShipmentFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('shipments', params)
        return result

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

    def get_project_by_pid(self, objid):
        """
        Get project based on project id
        @return: project 
        """
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

    def get_project_by_ref(self, ref):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        limit = params.get("limit")
        if 0 == limit:
            raise Exception("sorry, but a limit if 0 does not make sense, be sensible")
        result = self.call_list_api('members', params=params)
        return result

    def get_member_by_mid(self, objid):
        """
        Get member based on member id
        @return: member
        """
        result = self.call_get_api('members', objid=objid)
        return result

    def get_member_subscriptions_by_mid(self, objid):
        """
        Get member subscriptions based on member id
        @return: list of member subscriptions
        """
        objid = str(objid) + '/subscriptions'
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_id(self, objid):
        """
        Get member based on thirdparty id
        @return: member
        """
        objid = 'thirdparty/' + str(objid)
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_barcode(self, barcode):
        """
        Get member based on thirdparty barcode
        @return: member
        """
        objid = 'thirdparty/barcode/' + str(barcode)
        result = self.call_get_api('members', objid)
        return result

    def get_member_by_thirdparty_email(self, email):
        """
        Get member based on thirdparty email
        @return: member
        """
        objid = 'thirdparty/email/' + str(email)
        result = self.call_get_api('members', objid)
        return result

    def find_all_member_types(self, from_MemberFilter = None):
        """
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
        search_filter.page = page
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
        search_filter.page = page
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('thirdparties', params)
        return result

    def get_thirdparty_by_tid(self, objid):
        """
        Get thirdparty based on thirdparty id
        @return: thirdparty
        """
        result = self.call_get_api('thirdparties', objid=objid)
        return result

    def get_thirdparty_by_barcode(self, barcode):
        """
        Get thirdparty from barcode
        @return: thirdparty
        """
        objid = 'barcode/' + str(barcode)
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparty_by_email(self, email):
        """
        Get member based on thirdparty email
        @return: thirdparty
        """
        objid = 'email/' + str(email)
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_bankaccounts_by_tid(self, objid):
        """
        Get thirdparty bankaccounts based on thirdparty id
        @return: list of thirdparty bankaccounts
        """
        objid = str(objid) + '/bankaccounts'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_getinvoicesqualifiedforcreditnote_by_tid(self, objid):
        """
        Get thirdparty invoices qualifiedforcreditnote based on thirdparty id
        @return: list of thirdparty invoices qualifiedforcreditnote
        """
        objid = str(objid) + '/getinvoicesqualifiedforcreditnote'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_getinvoicesqualifiedforreplacement_by_tid(self, objid):
        """
        Get thirdparty invoices qualifiedforreplacement based on thirdparty id
        @return: list of thirdparty invoices qualifiedforreplacement
        """
        objid = str(objid) + '/getinvoicesqualifiedforreplacement'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_notifications_by_tid(self, objid):
        """
        Get thirdparty notifications based on thirdparty id
        @return: list of thirdparty notifications
        """
        objid = str(objid) + '/notifications'
        result = self.call_get_api('thirdparties', objid)
        return result

    def get_thirdparties_outstanding_by_tid(self, objid, otype, mode):
        """
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
        search_filter.page = page
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
        Get thirdparty generateBankAccountDocument based on thirdparty id, companybankid and model
        @companybankid
        @model default is 'sepamandate'
        @return: list of thirdparty's accounts
        """
        objid = str(objid) + '/generateBankAccountDocument/' + str(companybankid) + '/' + str(model)
        result = self.call_get_api('thirdparties', objid)
        return result


    # CONTACTS
    def find_all_contacts(self, from_ContactFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('contacts', params)
        return result

    def get_contact_by_cid(self, objid, includecount = 0, includeroles = 0):
        """
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
        search_filter.page = page
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

    # SUBSCRIPTIONS
    def find_all_subscriptions(self, from_SubscriptionFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('subscriptions', params)
        return result

    def get_subscription_by_sid(self, objid):
        """
        Get subscription based on subscription id
        @return: subscription
        """
        result = self.call_get_api('subscriptions', objid=objid)
        return result

    # PROPOSALS
    def find_all_proposals(self, from_ProposalFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('proposals', params)
        return result

    def get_proposal_by_pid(self, objid, contact_list = 1):
        """
        Get proposal based on proposal id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: proposal
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('proposals', objid=objid)
        return result

    def get_proposal_by_ref(self, objref, contact_list = 1):
        """
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
        Get proposal based on proposal ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: proposal
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('proposals', objid=objref_ext)
        return result

    def get_proposal_lines_by_pid(self, objid, sqlfilters):
        """
        Get proposal lines based on proposal id
        @sqlfilters string Other criteria to filter answers separated by a comma. d is the alias for proposal lines table, p is the alias for product table. "Syntax example "(p.ref:like:'SO-%') AND (d.date_start:
        @return: proposal lines
        """
        objid = str(objid) + '/lines?sqlfilters=' + str(sqlfilters)
        result = self.call_get_api('proposals', objid=objid)
        return result

    # ORDERS
    def find_all_orders(self, from_OrderFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('orders', params)
        return result

    def get_order_by_oid(self, objid, contact_list = 1):
        """
        Get order based on order id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: order
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('orders', objid=objid)
        return result

    def get_order_contacts_by_oid(self, objid, ctype = ''):
        """
        Get order based on order id and contact type
        @ctype string Type of the contact (BILLING, SHIPPING, CUSTOMER)
        @return: order
        """
        objid = str(objid) + '/contacts?type=' + str(ctype)
        result = self.call_get_api('orders', objid=objid)
        return result

    def get_order_by_ref(self, objref, contact_list = 1):
        """
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
        Get order based on order ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: order
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('orders', objid=objref_ext)
        return result

    def get_order_lines_by_oid(self, objid):
        """
        Get order lines based on order id
        @return: order lines
        """
        objid = str(objid) + '/lines'
        result = self.call_get_api('orders', objid=objid)
        return result

    def get_order_shipment_by_oid(self, objid):
        """
        Get order shipment based on order id
        @return: order shipment
        """
        objid = str(objid) + '/shipment'
        result = self.call_get_api('orders', objid=objid)
        return result

    # INVOICES
    def find_all_invoices(self, from_InvoiceFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('invoices', params)
        return result

    def get_invoice_by_iid(self, objid, contact_list = 1):
        """
        Get invoice based on invoice id
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice
        """
        objid = str(objid) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_discounts_by_iid(self, objid):
        """
        Get invoice discounts based on invoice id
        @return: discount
        """
        objid = str(objid) + '/discount'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_by_ref(self, objref, contact_list = 1):
        """
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
        Get invoice based on invoice ref_ext
        @contact_list int 1: Return array contains just id (default), 0: Returned array of contacts/addresses contains all properties
        @return: invoice
        """
        objref_ext = 'ref_ext/' + urllib.parse.quote(objref_ext) + '?contact_list=' + str(contact_list)
        result = self.call_get_api('invoices', objid=objref_ext)
        return result

    def get_invoice_lines_by_iid(self, objid):
        """
        Get invoice lines based on invoice id
        @return: invoice lines
        """
        objid = str(objid) + '/lines'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_payments_by_iid(self, objid):
        """
        Get invoice payments based on invoice id
        @return: invoice payments
        """
        objid = str(objid) + '/payments'
        result = self.call_get_api('invoices', objid=objid)
        return result

    def get_invoice_template_by_tid(self, objid, contact_list = 1):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('interventions', params)
        return result

    def get_intervention_by_iid(self, objid):
        """
        Get intervention based on intervention id
        @return: invoice
        """
        objid = str(objid)
        result = self.call_get_api('interventions', objid=objid)
        return result


    # TICKETS
    def find_all_tickets(self, from_TicketFilter = None):
        """
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
        search_filter.page = page
        params = asdict(search_filter)
        result = self.call_list_api('tickets', params)
        return result

    def get_ticket_by_iid(self, objid):
        """
        Get ticket based on ticket id
        @return: invoice
        """
        objid = str(objid)
        result = self.call_get_api('tickets', objid=objid)
        return result

    def get_ticket_by_ref(self, objref):
        """
        Get ticket based on ticket ref
        @return: invoice
        """
        objref = 'ref/' + str(objref)
        result = self.call_get_api('tickets', objid=objref)
        return result

    def get_ticket_by_track_id(self, objtrack_id):
        """
        Get ticket based on ticket track_id
        @return: invoice
        """
        objtrack_id = 'track_id/' + str(objtrack_id)
        result = self.call_get_api('tickets', objid=objtrack_id)
        return result
