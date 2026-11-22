"""Shared test data for R2 check_permission tests (Member 4)."""
from stock_control.models import User
from stock_control.store import Store


def make_store():
    """Store with one user per role plus one user whose role is not known:
    david (admin), alex (manager), christen (clerk), ghost (guest)."""
    store = Store()
    store.users["david"] = User("david", "pass123", "admin")
    store.users["alex"] = User("alex", "pass123", "manager")
    store.users["christen"] = User("christen", "pass123", "clerk")
    store.users["ghost"] = User("ghost", "pass123", "guest")
    return store
