from getpass import getpass
from hashlib import sha256
import os
import choice
import json
from config import parse_config


def login():
    #TODO this will be replaced by the config parser.
    ## ---------------------------------------------
    config = parse_config()
    filepath_complete = f"{os.path.expanduser("~")}/{config["hashpath"]}/{config["hashfile"]}"
    ## ---------------------------------------------
    did_hashfile_exist = True


    if not os.path.exists(filepath_complete):
        create_hashfile(filepath_complete)
        # TODO MESSY. REFACTOR ASAP
        create_hashfile(f"{os.path.expanduser(config["location"])}/{config["hashpath"]}/{config["saltfile"]}")
        create_saltfile(f"{os.path.expanduser(config["location"])}/{config["hashpath"]}/{config["saltfile"]}", os.urandom(16))
        did_hashfile_exist = False


    login_details = {"username": "", "password": ""}
    print("Since this is your first time accessing this program you will need to set up a new login.") if not did_hashfile_exist else None
    login_details["username"] = input("Username: ")
    login_details["password"] = getpass()

    hashed_login = sha256(json.dumps(login_details).encode()).hexdigest()

    if not did_hashfile_exist:
        create_hashfile(filepath_complete, hashed_login)
        return 200, login_details

    if parse_hashfile(filepath_complete) == hashed_login:
        return 200, login_details
    else:
        return 401, "Access denied."
    

def create_hashfile(filepath: str, data: str = ""):
    """Will create a hashfile if not there. If data passed to the function it will write to file."""

    with open(filepath, "w+") as f:
        f.write(data) if data else None
        f.close()

def create_saltfile(filepath: str, data: bytes):
    with open(filepath, "wb") as f:
        f.write(data)
        f.close()

def parse_saltfile(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()


def parse_hashfile(filepath: str) -> str:
    #TODO may choose to parse from config here.
    with open(filepath, "r") as file:
        return file.readline()