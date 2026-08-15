import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Render Secret File is available at /etc/secrets/
RENDER_CREDENTIALS_FILE = "/etc/secrets/credentials.json"

# Local development fallback
LOCAL_CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials.json"
)

TOKENS_DIR = os.path.join(
    BASE_DIR,
    "tokens"
)

os.makedirs(
    TOKENS_DIR,
    exist_ok=True
)


def get_credentials_file():

    if os.path.exists(
        RENDER_CREDENTIALS_FILE
    ):
        return RENDER_CREDENTIALS_FILE

    if os.path.exists(
        LOCAL_CREDENTIALS_FILE
    ):
        return LOCAL_CREDENTIALS_FILE

    raise FileNotFoundError(
        "credentials.json not found."
    )


def get_token_file(user_id: int):

    return os.path.join(
        TOKENS_DIR,
        f"user_{user_id}.json"
    )


def delete_user_gmail_token(user_id: int):

    token_file = get_token_file(
        user_id
    )

    if os.path.exists(token_file):
        os.remove(token_file)


def get_gmail_credentials(
    user_id: int,
    force_reauth: bool = False
):

    token_file = get_token_file(
        user_id
    )

    credentials = None

    if force_reauth:
        delete_user_gmail_token(
            user_id
        )

    if os.path.exists(token_file):

        try:

            credentials = (
                Credentials.from_authorized_user_file(
                    token_file,
                    SCOPES
                )
            )

        except Exception:
            credentials = None

    if (
        credentials
        and credentials.expired
        and credentials.refresh_token
    ):

        try:

            credentials.refresh(
                Request()
            )

        except Exception:

            credentials = None

    if credentials and credentials.valid:
        return credentials

    raise Exception(
        "Gmail is not connected. Please connect your Google account first."
    )


def create_google_flow():

    credentials_file = get_credentials_file()

    flow = Flow.from_client_secrets_file(
        credentials_file,
        scopes=SCOPES
    )

    flow.redirect_uri = (
        "https://cybershiledai-gg60.onrender.com/gmail/oauth/callback"
    )

    return flow


def save_credentials(
    user_id: int,
    credentials
):

    token_file = get_token_file(
        user_id
    )

    with open(
        token_file,
        "w"
    ) as token:

        token.write(
            credentials.to_json()
        )
        