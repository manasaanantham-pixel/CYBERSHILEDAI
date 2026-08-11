import os

from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CREDENTIALS_FILE = os.path.join(
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

    

    if not credentials or not credentials.valid:

        if not os.path.exists(
            CREDENTIALS_FILE
        ):

            raise FileNotFoundError(
                "credentials.json not found inside backend folder."
            )

        flow = (
            InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
        )

        credentials = flow.run_local_server(

            port=0,

            prompt="select_account",

            access_type="offline"
        )


    with open(
        token_file,
        "w"
    ) as token:

        token.write(
            credentials.to_json()
        )

    return credentials