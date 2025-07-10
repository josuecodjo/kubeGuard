# from streamlit_authenticator.hasher import Hasher
from streamlit_authenticator import Authenticate

def setup_auth():
    names = ["Josh Admin"]
    usernames = ["josh"]
    passwords = ["1234"]

    # Hash passwords
    hashed_passwords = Hasher(passwords).generate()

    credentials = {
        "usernames": {
            usernames[i]: {
                "name": names[i],
                "password": hashed_passwords[i]
            }
            for i in range(len(usernames))
        }
    }

    authenticator = Authenticate(
        credentials,
        "kubeshield_dashboard",
        "auth_cookie",
        cookie_expiry_days=1
    )

    return authenticator
