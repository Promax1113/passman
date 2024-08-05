from fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .login import parse_saltfile
from config import parse_config
import base64, json, os


def gen_fernet_key(login: bytes) -> Fernet:
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
    f = gen_fernet_key(json.dumps(login).encode())
    conf = parse_config()
    with open(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{filename}.enc", "rb") as file:
        return json.loads(f.decrypt(file.read()).decode())
    
def create_password(password: dict, login: dict):
    f = gen_fernet_key(json.dumps(login).encode())
    conf = parse_config()
    with open(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{password["name"]}.enc", "wb") as file:
        file.write(f.encrypt(json.dumps(password).encode()))