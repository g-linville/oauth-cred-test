import datetime
import json
import requests
import secrets
import string


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def capitalize_first_letter(s: str) -> str:
    return s[0].upper() + s[1:]


def print_cred(r: requests.Response):
    cred = {
        "env": {
            "GPTSCRIPT_API_SPOTIFY_COM_BEARER_TOKEN": r.json()["access_token"],
        },
        "refreshToken": r.json()["refresh_token"],
        "expiresAt": (datetime.datetime.utcnow() + datetime.timedelta(seconds=r.json()["expires_in"])).replace(microsecond=0).isoformat() + "Z",
    }
    print(json.dumps(cred))
