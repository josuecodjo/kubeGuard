import streamlit_authenticator as stauth

def setup_auth():
    # Replace these with real users and hashed passwords
    names = ["Josh Admin"]
    usernames = ["josh"]
    passwords = ["1234"]  # plaintext for dev only

    # Hash the passwords
    hashed_passwords = stauth.Hasher(passwords).generate()

    credentials = {
        "usernames": {
            usernames[i]: {
                "name": names[i],
                "password": hashed_passwords[i]
            }
            for i in range(len(usernames))
        }
    }

    authenticator = stauth.Authenticate(
        credentials,
        "kubeshield_dashboard",
        "auth_cookie",
        cookie_expiry_days=1
    )

    return authenticator
