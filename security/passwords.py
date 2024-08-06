import base64
import json
import os

from fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import parse_config

from .login import parse_saltfile

def gen_fernet_key(login: bytes) -> Fernet:
    """Generates a fernet key using PKBDF2HMAC and a salt."""
    conf = parse_config()
    saltfile = conf["saltfile"]
    hashpath = conf["hashpath"]
    salt = parse_saltfile(f"{os.path.expanduser(conf["location"])}/{hashpath}/{saltfile}")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, salt=salt,
        iterations=390000
        )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(login)))


def read_password(filename: str, login: dict) -> dict:
    """Reads the encrypted password from a file and decrypts it."""
    f = gen_fernet_key(json.dumps(login).encode())
    conf = parse_config()
    with open(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{filename}.enc", "rb") as file:
        return json.loads(f.decrypt(file.read()).decode())


def write_password(password: dict, login: dict, changed_name: bool = False, old_name: str = None):
    """Writes the password to the file and encrypts it."""
    f = gen_fernet_key(json.dumps(login).encode())
    conf = parse_config()
    with open(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{password["name"]}.enc", "wb") as file:
        file.write(f.encrypt(json.dumps(password).encode()))

    if changed_name:
        os.remove(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{old_name}.enc")
