from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_master_password(password):
    return ph.hash(password)

def verify_master_password(hash, password):
    try:
        ph.verify(hash, password)
        return True
    except:
        return False

        