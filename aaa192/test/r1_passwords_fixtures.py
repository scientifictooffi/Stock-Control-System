"""Shared test data for the R1 password hashing follow-up (Member 4)."""
import hashlib

from stock_control.models import User
from stock_control.reporting.passwords import ITERATIONS, hash_password
from stock_control.store import Store

SALT = "a1" * 16
PASSWORD = "pass123"


def expected_hash(password, salt=SALT):
    """Oracle written straight from the rules: PBKDF2-SHA256 of the
    password with the salt, stored as "salt$hash"."""
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt), ITERATIONS)
    return salt + "$" + digest.hex()


def make_store():
    """Store with three users:
    sam - password "pass123" stored hashed with SALT
    old - password stored in plain text (no salt)
    odd - stored value contains "$" but the salt part is not hex
    """
    store = Store()
    store.users["sam"] = User("sam", hash_password(PASSWORD, SALT), "admin")
    store.users["old"] = User("old", PASSWORD, "clerk")
    store.users["odd"] = User("odd", "zz$abc", "manager")
    return store
