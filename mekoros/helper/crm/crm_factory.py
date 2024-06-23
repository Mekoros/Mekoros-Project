from mekoros import settings as sls
from mekoros.helper.crm.nationbuilder import NationbuilderConnectionManager
from mekoros.helper.crm.salesforce import SalesforceConnectionManager
from mekoros.helper.crm.dummy_crm import DummyConnectionManager


class CrmFactory(object):
    def __init__(self):
        self.crm_type = sls.CRM_TYPE

    def get_connection_manager(self):
        if self.crm_type == "NATIONBUILDER":
            return NationbuilderConnectionManager()
        elif self.crm_type == "SALESFORCE":
            return SalesforceConnectionManager()
        elif self.crm_type == "NONE" or not self.crm_type:
            return DummyConnectionManager()
        else:
            return DummyConnectionManager()
