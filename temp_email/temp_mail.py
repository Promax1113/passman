import requests

URL = "https://www.1secmail.com/api/v1/"



def get_email_address():
    """Gets a random email address from the API at 1secmail.com"""
    global URL

    get_email = "?action=genRandomMailbox&count=1"
    return "".join(requests.get(f"{URL}{get_email}").json())

def check_inbox(email: str):
    """Checks the whole inbox and returns it."""
    
    global URL

    user  = email.split("@")[0]
    domain = email.split("@")[1]
    get_inbox = f"?action=getMessages&login={user}&domain={domain}"

    return requests.get(f"{URL}{get_inbox}").json()

def check_email_in_inbox(email: str, email_id: int):
    """Checks the last email in the email provided using the API."""
    global URL
    user  = email.split("@")[0]
    domain = email.split("@")[1]
    action = "/?action=readMessage&login={user}&domain={domain}&id={email_id}"
    return requests.get(f"{URL}{action}").text

