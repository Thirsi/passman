import secrets
import string
import pyperclip
import time


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("Password copied to clipboard. Clearing in 10 seconds...")
    time.sleep(10)
    pyperclip.copy("")