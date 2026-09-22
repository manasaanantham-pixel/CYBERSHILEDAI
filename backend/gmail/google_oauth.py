import os
import json

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GOOGLE SCOPES
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# =========================================================
# GOOGLE OAUTH SETTINGS
# =========================================================

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
print("GOOGLE REDIRECT URI:", REDIRECT_URI)

# =========================================================
# TOKEN DIRECTORY
# =========================================================

TOKEN_DIR = os.path.join(
    os.path.dirname(__file__),
    "tokens"
)

os.makedirs(
    TOKEN_DIR,
    exist_ok=True
)


# =========================================================
# CREATE GOOGLE OAUTH FLOW
# =========================================================

def create_google_flow():

    if not CLIENT_ID:
        raise RuntimeError(
            "GOOGLE_CLIENT_ID is missing."
        )

    if not CLIENT_SECRET:
        raise RuntimeError(
            "GOOGLE_CLIENT_SECRET is missing."
        )

    if not REDIRECT_URI:
        raise RuntimeError(
            "GOOGLE_REDIRECT_URI is missing."
        )

    client_config = {
        "web": {
            "client_id": CLIENT_ID,

            "client_secret": CLIENT_SECRET,

            "auth_uri":
                "https://accounts.google.com/o/oauth2/auth",

            "token_uri":
                "https://oauth2.googleapis.com/token",

            "redirect_uris": [
                REDIRECT_URI
            ]
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    return flow


# =========================================================
# GET TOKEN PATH
# =========================================================

def get_token_path(user_id: int):

    return os.path.join(
        TOKEN_DIR,
        f"user_{user_id}.json"
    )


# =========================================================
# SAVE GOOGLE CREDENTIALS
# =========================================================

def save_credentials(
    user_id: int,
    credentials
):

    token_path = get_token_path(
        user_id
    )

    data = {
        "token": credentials.token,

        "refresh_token": credentials.refresh_token,

        "token_uri": credentials.token_uri,

        "client_id": credentials.client_id,

        "client_secret": credentials.client_secret,

        "scopes": credentials.scopes
    }

    with open(
        token_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# =========================================================
# LOAD GOOGLE CREDENTIALS
# =========================================================

def load_credentials(
    user_id: int
):

    token_path = get_token_path(
        user_id
    )

    if not os.path.exists(
        token_path
    ):
        return None

    try:

        credentials = (
            Credentials.from_authorized_user_file(
                token_path,
                SCOPES
            )
        )

        return credentials

    except Exception as error:

        print(
            "LOAD GOOGLE TOKEN ERROR:",
            str(error)
        )

        return None


# =========================================================
# GET GMAIL CREDENTIALS
# =========================================================

def get_gmail_credentials(
    user_id: int
):

    credentials = load_credentials(
        user_id
    )

    if credentials is None:

        raise RuntimeError(
            "Gmail is not connected for this user."
        )

    # -----------------------------------------------------
    # Refresh expired access token
    # -----------------------------------------------------

    if (
        credentials.expired
        and credentials.refresh_token
    ):

        try:

            credentials.refresh(
                Request()
            )

            save_credentials(
                user_id,
                credentials
            )

        except Exception as error:

            print(
                "GOOGLE TOKEN REFRESH ERROR:",
                str(error)
            )

            raise RuntimeError(
                "Gmail session expired. "
                "Please reconnect Gmail."
            )

    # -----------------------------------------------------
    # Check credentials
    # -----------------------------------------------------

    if not credentials.valid:

        raise RuntimeError(
            "Gmail credentials are invalid. "
            "Please reconnect Gmail."
        )

    return credentials


# =========================================================
# DELETE USER GMAIL TOKEN
# =========================================================

def delete_user_gmail_token(
    user_id: int
):

    token_path = get_token_path(
        user_id
    )

    if os.path.exists(
        token_path
    ):

        os.remove(
            token_path
        )

        print(
            f"Deleted Gmail token for user {user_id}"
        )

    return True