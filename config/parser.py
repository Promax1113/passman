from configparser import ConfigParser
import os

def parse_config():
    conf = ConfigParser()
    conf.read(f"{os.getcwd}/config/config.cfg")
    return {
        "hashfile": conf.get("user.settings", "hashfile", fallback=conf.get("DEFAULT", "hashfile")),
        "hashpath": conf.get("user.settings", "hashpath", fallback=conf.get("DEFAULT", "hashpath")),
        "location": conf.get("user.settings", "location", fallback=conf.get("DEFAULT", "location"))
        }