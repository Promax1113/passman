from security import login, create_password, read_password


result = 401

while result == 401:
    result, message = login()
    if result == 401:
        print(message)
    else:
        break

print("Acess granted!")


create_password({"name": "google", "data": "yessir"}, message)
print(read_password("google", message))