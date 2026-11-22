import hashlib
import secrets

SALT_BYTES = 16
ITERATIONS = 10_000
SEPARATOR = "$"


def hash_password(password, salt=None):
    """R1 follow-up (Member 4): store passwords hashed with salt, never in
    plain text.

    Rules:
        1. Password must be a non-empty string
        2. A new random salt is made when no salt is given
        3. A given salt must be a non-empty hex string
        4. Same password and same salt always give the same result
        5. Result is "salt$hash" and never contains the plain password

    Returns the stored form "salt$hash" (both hex).
    Raises ValueError when a rule fails.
    """
    # Rule 1: password must be a non-empty string
    if not isinstance(password, str) or password == "":
        raise ValueError("password must be a non-empty string")
    # Rule 2: make a new random salt when none is given
    if salt is None:
        salt = secrets.token_hex(SALT_BYTES)
    # Rule 3: a given salt must be a non-empty hex string
    if not isinstance(salt, str) or salt == "":
        raise ValueError("salt must be a non-empty hex string")
    try:
        salt_bytes = bytes.fromhex(salt)
    except ValueError:
        raise ValueError("salt must be a non-empty hex string") from None
    # Rules 4 and 5: PBKDF2 is deterministic for the same input
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 salt_bytes, ITERATIONS)
    return salt + SEPARATOR + digest.hex()


def hash_for_user(store, username, password):
    """R1 follow-up (Member 4): turn the password typed at login into the
    stored form, using the salt saved for that user, so that login() can
    compare it.

    Rules:
        1. Unknown user: the typed password is returned unchanged
           (login() then refuses the username)
        2. Empty password: returned unchanged (login() counts a wrong try)
        3. Stored password not in "salt$hash" form: returned unchanged
        4. Otherwise: hashed with the user's own salt
    """
    user = store.users.get(username)
    # Rule 1: unknown user
    if user is None:
        return password
    # Rule 2: empty password
    if not isinstance(password, str) or password == "":
        return password
    # Rule 3: stored password not in "salt$hash" form
    if SEPARATOR not in user.password:
        return password
    salt = user.password.split(SEPARATOR, 1)[0]
    try:
        # Rule 4: hash with the user's salt
        return hash_password(password, salt)
    except ValueError:
        return password
