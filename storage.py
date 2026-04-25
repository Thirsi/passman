import json
import os

VAULT_FILE = "vault.json"


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return None

    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(data):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)