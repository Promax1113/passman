from getpass import getpass
from hashlib import sha256
import os
import choice
import json


def login():
    #TODO this will be replaced by the config parser.
    ## ---------------------------------------------
    filename = "hash.file"
    filepath = f"{os.path.expanduser("~")}/.passman/"
    filepath_complete = filepath + filename
    ## ---------------------------------------------
    did_hashfile_exist = True


    if not os.path.exists(filepath_complete):
        create_hashfile(filepath_complete)
        did_hashfile_exist = False


    login_details = {"username": "", "password": ""}
    print("Since this is your first time accessing this program you will need to set up a new login.") if not did_hashfile_exist else None
    login_details["username"] = input("Username: ")
    login_details["password"] = getpass()

    hashed_login = sha256(json.dumps(login_details).encode()).hexdigest()

    if not did_hashfile_exist:
        create_hashfile(filepath_complete, hashed_login)
        return 200

    if parse_hashfile(filepath_complete) == hashed_login:
        return 200
    else:
        return 401
    

def create_hashfile(filepath: str, data: str = ""):
    """Will create a hashfile if not there. If data passed to the function it will write to file."""

    with open(filepath, "w+") as f:
        f.write(data) if data else None
        f.close()


def parse_hashfile(filepath: str) -> str:
    #TODO may choose to parse from config here.

    with open(filepath, "r") as file:
        return file.readline()