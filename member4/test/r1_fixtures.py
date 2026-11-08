"""Shared test data for R1 login tests (Member 4)."""
from stock_control.models import User
from stock_control.store import Store


def make_store():
    """Store with three users: an active admin, an inactive clerk and a
    locked manager. Every password is "pass123"."""
    store = Store()
    store.users["sam"] = User("sam", "pass123", "admin")
    store.users["lee"] = User("lee", "pass123", "clerk", active=False)
    store.users["kim"] = User("kim", "pass123", "manager", locked=True,
                              failed_logins=3)
    return store
