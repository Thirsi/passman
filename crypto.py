import os
import base64
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

ph = PasswordHasher()


def hash_master_password(password):
    return ph.hash(password)


def verify_master_password(stored_hash, password):
    try:
        ph.verify(stored_hash, password)
        return True
    except:
        return False


def generate_salt():
    return os.urandom(16)


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt(key, text):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def decrypt(key, token):
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()