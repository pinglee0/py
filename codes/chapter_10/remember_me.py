import json

def get_stored_username():
    """Get stored username if available."""
    filename = 'username.json'
    try:
        with open(filename) as f:
            username = json.load(f)
    except FileNotFoundError:
        return None
    else:
        return username

def get_new_username():
    """Prompt for a new username."""
    username = input("What is your name? ")
    filename = 'username.json'
    with open(filename, 'r+') as f:
        jsonC = json.load(f)
        jsonC.append(username)
        json.dump(jsonC, f)
    return username

def greet_user(u):
    """Greet the user by name."""

    username = get_stored_username()
    if u in username:
        print(f"Welcome back, {username}!")
    else:
        username = get_new_username()
        print(f"We'll remember you when you come back, {username}!")
while True:
    a = input("username:")
    if a=="q":
        break
    if a=="all":
        with open('username.json') as f:
            username = json.load(f)
            print(username)
    greet_user(a)

