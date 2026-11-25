import copy
from stock_control.models import Supplier
from stock_control.store import Store

ACTIVE_ID = "SUP0001"
SUSPENDED_ID = "SUP0002"
UNKNOWN_ID = "SUP9999"
ACTIVE_NAME = "Acme Plumbing Ltd"
SUSPENDED_NAME = "Delta Tools"
NEW_NAME = "Midlands Pipe Co"
EMAIL = "sales@midlandspipe.co.uk"
PHONE = "+44 116 496 0000"


def make_store():
    store = Store()
    store.suppliers = {
        ACTIVE_ID: Supplier(
            ACTIVE_ID, ACTIVE_NAME, "orders@acme.co.uk", "0116 496 0001",
            min_order_value=50.0, deliveries_on_time=4, deliveries_total=5),
        SUSPENDED_ID: Supplier(
            SUSPENDED_ID, SUSPENDED_NAME, "hello@delta.co.uk",
            "0116 496 0002", status="suspended"),
    }
    return store


def snapshot(store):
    return copy.deepcopy(store)
