import string
import random

import choice


def generate_password():
    """Generates a password from all ascii characters, numbers and some symbols."""
    password = "undefined"
    chars = string.ascii_uppercase + string.ascii_lowercase + "1234567890" + r"$%&()=?{}!*^"
    ok = False
    while not ok:
        length = choice.Input("Enter the desired length", int).ask()

        password = "".join(random.choices(chars, k=length))

        ok = choice.Binary(f"Is the password '{password}' okay?", default=True).ask()
        if ok:
            break

    return password
    