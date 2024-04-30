import argparse
import datetime
import json
import os
import requests
import signal
import sys
import time
import urllib.parse

from data import LOGIN_MANAGER_ENDPOINT, SERVICES, SCOPES, REFRESH_DOMAINS
from util import generate_random_string, capitalize_first_letter, print_cred

keep_running = True


# Set up signal handlers
def signal_handler(signum, frame):
    global keep_running
    keep_running = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Set up argparse
parser = argparse.ArgumentParser(description="Credential tool for OAuth integrations.")
parser.add_argument("service_name", type=str, help="The name of the service you are integrating with.",
                    choices=SERVICES)
args = parser.parse_args()


# If GPTSCRIPT_EXISTING_CREDENTIAL is set, then the existing credential is expired, and we need to refresh it.
existing_json = os.getenv("GPTSCRIPT_EXISTING_CREDENTIAL")
if existing_json:
    # First, get the client ID from the API
    resp = requests.get(f"{LOGIN_MANAGER_ENDPOINT}/api/get_client_id?service={args.service_name}")
    if resp.status_code != 200:
        print("An error occurred while fetching the client ID.", file=sys.stderr)
        exit(1)

    existing = json.loads(existing_json)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": urllib.parse.quote(existing["refresh_token"]),
        "client_id": urllib.parse.quote(resp.json()["client_id"]),
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = requests.post(REFRESH_DOMAINS[args.service_name], data=data, headers=headers)
    if resp.status_code != 200:
        print("An error occurred while refreshing the token.", file=sys.stderr)
        exit(1)
    print_cred(resp)
    exit(0)


# Generate a random state and send the user to the login page.
state = generate_random_string(128)
url = f"{LOGIN_MANAGER_ENDPOINT}/services/{args.service_name}?state={state}&scopes={urllib.parse.quote(' '.join(SCOPES[args.service_name]))}"
print(f"Please visit the following URL to log in to {capitalize_first_letter(args.service_name)}:\n{url}", file=sys.stderr)

# Start polling for the token
try:
    while keep_running:
        time.sleep(2)
        resp = requests.get(f"{LOGIN_MANAGER_ENDPOINT}/api/get_token?state={state}")
        if resp.status_code == 200:
            print_cred(resp)
            break
        elif resp.status_code != 404:
            print("An error occurred while fetching the token.", file=sys.stderr)
            exit(1)
except KeyboardInterrupt:
    exit(0)
