import getpass
import base64
from rich import print
from rich.console import Console
from rich.table import Table

from storage import load_vault, save_vault
from crypto import (
    hash_master_password,
    verify_master_password,
    generate_salt,
    derive_key,
    encrypt,
    decrypt
)
from utils import generate_password, copy_to_clipboard

console = Console()


def setup():
    console.print("[bold green]First-time setup[/bold green]")

    password = getpass.getpass("Create master password: ")

    salt = generate_salt()
    hashed_password = hash_master_password(password)

    data = {
        "salt": base64.b64encode(salt).decode(),
        "master_password_hash": hashed_password,
        "entries": []
    }

    save_vault(data)
    console.print("[green]Vault created successfully! Restart the app.[/green]")


def login(vault):
    password = getpass.getpass("Enter master password: ")

    if verify_master_password(vault["master_password_hash"], password):
        salt = base64.b64decode(vault["salt"])
        key = derive_key(password, salt)
        console.print("[bold green]Access granted[/bold green]")
        return key
    else:
        console.print("[bold red]Access denied[/bold red]")
        return None


def add_entry(vault, key):
    service = input("Service Name: ")
    username = input("Username/Email: ")
    password = getpass.getpass("Password (leave blank to generate): ")

    if password == "":
        password = generate_password()
        console.print(f"[yellow]Generated Password:[/yellow] {password}")

    encrypted_password = encrypt(key, password)

    vault["entries"].append({
        "service": service,
        "username": username,
        "password": encrypted_password
    })

    save_vault(vault)
    console.print("[green]Entry saved successfully[/green]")


def get_entry(vault, key):
    service = input("Enter service name to retrieve: ")

    for entry in vault["entries"]:
        if entry["service"].lower() == service.lower():
            decrypted_password = decrypt(key, entry["password"])

            table = Table(title="Stored Credential")
            table.add_column("Service")
            table.add_column("Username")
            table.add_column("Password")

            table.add_row(entry["service"], entry["username"], decrypted_password)

            console.print(table)

            choice = input("Copy password to clipboard? (y/n): ")
            if choice.lower() == "y":
                copy_to_clipboard(decrypted_password)
            return

    console.print("[red]No entry found.[/red]")


def delete_entry(vault):
    service = input("Enter service name to delete: ")

    for entry in vault["entries"]:
        if entry["service"].lower() == service.lower():
            vault["entries"].remove(entry)
            save_vault(vault)
            console.print("[green]Entry deleted.[/green]")
            return

    console.print("[red]No entry found.[/red]")


def list_entries(vault):
    if not vault["entries"]:
        console.print("[yellow]No saved entries.[/yellow]")
        return

    table = Table(title="Saved Services")
    table.add_column("Service")
    table.add_column("Username")

    for entry in vault["entries"]:
        table.add_row(entry["service"], entry["username"])

    console.print(table)


def menu(vault, key):
    while True:
        console.print("\n[bold cyan]Password Manager Menu[/bold cyan]")
        console.print("1. Add Password")
        console.print("2. Retrieve Password")
        console.print("3. Delete Password")
        console.print("4. List Saved Services")
        console.print("5. Generate Random Password")
        console.print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            add_entry(vault, key)
        elif choice == "2":
            get_entry(vault, key)
        elif choice == "3":
            delete_entry(vault)
        elif choice == "4":
            list_entries(vault)
        elif choice == "5":
            password = generate_password()
            console.print(f"[yellow]Generated Password:[/yellow] {password}")
        elif choice == "6":
            console.print("[cyan]Goodbye[/cyan]")
            break
        else:
            console.print("[red]Invalid option[/red]")


def main():
    vault = load_vault()

    if vault is None:
        setup()
    else:
        key = login(vault)
        if key:
            menu(vault, key)


if __name__ == "__main__":
    main()

    