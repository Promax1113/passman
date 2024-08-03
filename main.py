from security import login

result = 401

while result == 401:
    result, message = login()
    if result == 401:
        print(message)
    else:
        break

print("Acess granted!")
