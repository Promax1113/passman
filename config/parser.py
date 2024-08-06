from configparser import ConfigParser
import os
import pathlib

def parse_config():
    """Parses config from the default config file."""
    conf = ConfigParser()
    conf.read(f"{os.getcwd}/config/config.cfg")
    # TODO REFACTOR OR RETHINK
    conf = {
        "hashfile": conf.get("user.settings", "hashfile", fallback="hash.file"),
        "hashpath": conf.get("user.settings", "hashpath", fallback=".passman"),
        "location": conf.get("user.settings", "location", fallback="~"),
        "saltfile": conf.get("user.settings", "saltfile", fallback="salt.file")
        }
    pathlib.Path(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}").mkdir(exist_ok=True)
    pathlib.Path(
        f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords").mkdir(exist_ok=True)
    return conf
