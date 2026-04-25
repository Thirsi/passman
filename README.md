# 🔐 Python Password Manager

A secure command-line password manager built in Python that stores user credentials in an encrypted local JSON vault.

This project was created as a practical cybersecurity and Python development exercise, demonstrating:

- password hashing
- key derivation
- symmetric encryption
- secure local storage
- clipboard integration
- command-line UI design

---

## 📌 Features

- Master password authentication
- Argon2 password hashing
- PBKDF2 key derivation
- Fernet AES encryption for stored passwords
- Local JSON vault storage
- Add / retrieve / delete credentials
- Secure random password generation
- Optional clipboard copy support
- Rich formatted terminal interface

---

## 🔒 Security Overview

This application uses multiple layers of protection to prevent stored credentials from being read without the master password.

### Master Password Protection

The master password is never stored in plaintext.

Instead, it is hashed using **Argon2**, a modern password hashing algorithm designed to resist brute-force attacks.

---

### Encryption Key Derivation

After successful login, the application derives a secure encryption key from:

- the entered master password
- a randomly generated salt

using **PBKDF2-HMAC-SHA256**.

This key exists only in memory during runtime.

---

### Stored Password Encryption

Each saved credential password is encrypted using **Fernet symmetric encryption** before being written to disk.

Without the master password, encrypted passwords inside `vault.json` cannot be decrypted.

---

## ⚠ Important Note

Current version encrypts stored passwords only.

Service names and usernames remain visible in the JSON file.

A future version will encrypt the full vault entries for improved metadata privacy.

---

## 📁 Project Structure

```text
password_manager/
│── main.py
│── crypto.py
│── storage.py
│── utils.py
│── vault.json
│── README.md
```

---

## 📦 Required Libraries

Install dependencies:

```bash
pip install cryptography argon2-cffi pyperclip rich
```

---

## 🐧 Linux Clipboard Support

`pyperclip` requires a clipboard backend on Linux.

Install one of the following:

```bash
sudo apt-get install xclip
```

or

```bash
sudo apt-get install xsel
```

or (Wayland)

```bash
sudo apt-get install wl-clipboard
```

---

## ▶ Running the Application

From inside the project directory:

```bash
python main.py
```

On first launch the program will:

1. ask you to create a master password
2. generate a secure salt
3. create `vault.json`

Subsequent launches require the master password for access.

---

## 🧠 How It Works

### Add Password
Stores:
- service name
- username/email
- encrypted password

---

### Retrieve Password
Decrypts the stored password in memory after authentication.

Optionally copies it to clipboard for 10 seconds.

---

### Delete Password
Removes the selected entry from the local vault.

---

### Generate Password
Creates a cryptographically secure random password using Python's `secrets` module.

---

## 📄 Example Vault File

```json
{
    "salt": "stored_salt_here",
    "master_password_hash": "argon2_hash_here",
    "entries": [
        {
            "service": "gmail",
            "username": "example@gmail.com",
            "password": "gAAAAAB..."
        }
    ]
}
```

---

## 🚧 Planned Improvements (Version 2)

- full vault encryption
- credential editing
- search by partial service name
- failed login lockout
- session timeout
- automatic vault backups
- GUI version
- import/export support

---

## 👨‍💻 Author

Created by Henry as part of a practical Python security project.