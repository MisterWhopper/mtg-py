import os
import sys
import json
import platform

BASE_PATH = os.path.abspath(os.path.dirname(__file__)) # get the directory the script itself is running from

HELP_STR = """
Usage: mtg <name>
       mtg new

Where name is the custom name of the meeting to open, stored in 'config.json' in the installation directory (override with $MTG_CONF env variable)
"""

def find_file():
    fp = f"{BASE_PATH}/config.json"
    if "MTG_CONF" in os.environ.keys():
        fp = os.environ["MTG_CONF"]
    if os.path.isfile(fp):
        return fp
    sys.stderr.write(f"Configuration file not found @ '{fp}''. Please either create missing file or update $MTG_CONF env variable\n")
    sys.exit(2)

def load_data():
    data = None
    fp = find_file()
    with open(fp,"r") as f:
        data = json.loads(f.read())
    return data

def new_user(data):
    fp = find_file()
    print("Creating new user entry")
    name = input("Name: ")
    if name in data.keys():
        print(f"WARNING: '{name}' already exists.")
        conf = input("Override? [Y/N]: ").lower()
        if "n" == conf[0]:
            return
    link = input("Link: ")
    browser = input("Browser (default firefox): ")
    browser = browser if browser != "" else None
    password = input("Password (optional): ")
    password = password if password != "" else None
    data[name] = {"link":link,"browser":browser, "password":password}
    with open(fp, "w") as f:
        f.write(json.dumps(data))
    print(f"{name} added to database!")
    conf = input("Continue defining new entries? [Y/N]: ").lower()
    if "y" == conf[0]:
        new_user(data)

def main():
    data = load_data()
    if data is None:
        sys.stderr.write("ERROR: config file either empty or read error encountered.\n")
        sys.exit(1)
    if len(sys.argv) <= 1:
        print(HELP_STR)
        sys.exit(0)
    if sys.argv[1].lower() != "new":
        if sys.argv[1] in data.keys():
            link = data[sys.argv[1]]["link"]
            browser = data[sys.argv[1]]["browser"] if data[sys.argv[1]]["browser"] is not None else "firefox"
            extra = "</dev/null &>/dev/null &" if platform.system()=="Linux" else ""
            os.system(f"{browser} {link} {extra}")
    else: # if the user is trying to define a new user
        new_user(data)

if __name__ == "__main__":
    main()