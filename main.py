from security import login, create_password, read_password
import choice, os, time
from config import parse_config


result = 401

while result == 401:
    result, login_details = login()
    if result == 401:
        print(login_details)
    else:
        break

print("Acess granted!")

conf = parse_config()

while True:
    match choice.Menu(["read or edit a password", "create a password", "settings", "exit"]).ask():
        case "read or edit a password":
            passwords = ["".join(password.split(".")[:-1]) for password in os.listdir(f"{os.path.expanduser(conf["location"])}/{conf["hashpath"]}/passwords/")]
            if len(passwords) == 0:
                print("\nThere are no passwords saved!\n")
                time.sleep(1)
                continue
            name, action = choice.Menu(choices=passwords, actions=["read", "edit", "delete"]).ask()
            match action:
                case "read":
                    read_password(name, login_details)
                case "edit":
                    continue
                case "delete":
                    os.remove(f"{name}.enc") if choice.Binary(prompt="Are you sure you want to delete this password named {name}?", default=False).ask() else None

        case "create a password":
            pass
        case "exit":
            exit()
    
