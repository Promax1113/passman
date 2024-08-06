import os
import time
import getpass

import choice


from security import login, write_password, read_password, generate_password
from config import parse_config


def clear_screen():
    """Clears the screen by running the correct command for the os."""
    os.system("cls" if os.name == "nt" else "clear")

result = 401

while result == 401:
    result, login_details = login()
    if result == 401:
        print(login_details)
    else:
        break

print("Acess granted!")
time.sleep(0.5)
conf = parse_config()

while True:
    clear_screen()
    match choice.Menu(["read or edit a password", "create a password", "generate a password", "exit"]).ask():
        case "read or edit a password":
            passwords = ["".join(password.split(".")[:-1]) for password in os.listdir(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/")]
            if len(passwords) == 0:
                print("\nThere are no passwords saved!\n")
                time.sleep(1)
                continue
            name, action = choice.Menu(choices=passwords, actions=["read", "edit", "delete"]).ask()
            match action:
                case "read":
                    clear_screen()
                    password = read_password(name, login_details)
                    for key in password.keys():
                        print(f"{key}: {password[key]}")
                    input("\npress enter to continue...")
                case "edit":
                    changed_name = False
                    current_name = None
                    password = read_password(name, login_details)
                    clear_screen()
                    to_mod = choice.Menu(password.keys(), title="Choose which field to edit:").ask()
                    if to_mod == "name":
                        changed_name = True
                        current_name = password[to_mod]
                    print(f"current value: {password[to_mod]}")
                    new_val = input("new value (leave blank if same as previous): ")
                    password[to_mod] =  new_val if new_val else password[to_mod]
                    
                    write_password(password, login_details, changed_name=changed_name, old_name=current_name) if choice.Binary("Do you want to save the change", default=False).ask() else None

                case "delete":
                    os.remove(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/{name}.enc") if choice.Binary(prompt="Are you sure you want to delete this password named {name}?", default=False).ask() else None

        case "create a password":
            password = {"username": choice.Input("Enter your username on the page").ask(),
                        "password": getpass.getpass("Password on the website: "),
                        "note": choice.Input("Enter any note or leave blank").ask(),
                        "name": choice.Input("Enter any name or word to recognize this password easily").ask()
                        }
        
            write_password(password, login_details)

        case "generate a password":
            passwd = generate_password()
            print(f"Your password: \n\n{passwd}\n\n")
            input("press any enter to continue...")

        case "exit":
            clear_screen()
            exit()
            