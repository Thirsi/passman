import getpass
import os
from storage import load_vault, save_vault
from crypto import hash_master_password
from crypto import verify_master_password

def setup():
    print("First-time setup")

    password = getpass.getpass("Create master password: ")
    hashed = hash_master_password(password)

    data = {
        "salt": "",
        "master_password_hash": hashed,
        "entries": []
    }

    save_vault(data)

def login(vault):
    password = getpass.getpass("Enter master password: ")

    if verify_master_password(vault["master_password_hash"], password):
        print("Access granted")
        return password
    else:
        print("Access denied")
        return None

def main():
    vault = load_vault()

    if vault is None:
        setup()
    else:
        print("Vault exists")

if __name__ == "__main__":
    main()
