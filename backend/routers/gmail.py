from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User
from dependencies import get_current_user

from gmail.gmail_service import (
    get_profile,
    list_messages,
    get_message,
    extract_body,
    extract_attachments,
)

from gmail.google_oauth import (
    create_google_flow,
    save_credentials,
    delete_user_gmail_token,
)


router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"]
)


@router.get("/status")
def gmail_status(
    current_user: User = Depends(get_current_user)
):

    try:

        profile = get_profile(
            current_user.id
        )

        return {
            "success": True,
            "connected": True,
            "email": profile.get(
                "emailAddress",
                ""
            ),
            "messages_total": profile.get(
                "messagesTotal",
                0
            ),
            "threads_total": profile.get(
                "threadsTotal",
                0
            ),
        }

    except Exception:

        return {
            "success": True,
            "connected": False,
            "email": "",
            "messages_total": 0,
            "threads_total": 0,
        }



@router.get("/oauth/start")
def gmail_oauth_start(
    current_user: User = Depends(get_current_user)
):

    try:

        flow = create_google_flow()

        authorization_url, state = (
            flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
                prompt="select_account consent",
            )
        )

        return {
            "success": True,
            "authorization_url": authorization_url,
        }

    except Exception as error:

        print(
            "GMAIL OAUTH START ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )



@router.get("/oauth/callback")
def gmail_oauth_callback(
    request: Request,
    code: str = None,
    state: str = None,
):

    if not code:

        raise HTTPException(
            status_code=400,
            detail="Google authorization code missing."
        )

    try:

        flow = create_google_flow()

        flow.fetch_token(
            code=code
        )

        credentials = flow.credentials

        # IMPORTANT:
        # Google OAuth callback does not automatically
        # know our logged-in user.
        #
        # For the current simple version we use
        # the user ID passed through OAuth state.

        if not state:

            raise HTTPException(
                status_code=400,
                detail="OAuth state missing."
            )

        user_id = int(state)

        save_credentials(
            user_id,
            credentials
        )

        profile = get_profile(
            user_id
        )

        email = profile.get(
            "emailAddress",
            ""
        )

        frontend_url = (
            "https://cybershiledai.vercel.app"
        )

        return RedirectResponse(
            url=(
                f"{frontend_url}"
                f"/?gmail_connected=true"
                f"&email={email}"
            )
        )

    except Exception as error:

        print(
            "GMAIL OAUTH CALLBACK ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )



@router.get("/connect")
def connect_gmail(
    current_user: User = Depends(get_current_user)
):

    try:

        profile = get_profile(
            current_user.id
        )

        return {
            "success": True,
            "connected": True,
            "email": profile.get(
                "emailAddress",
                ""
            ),
            "messages_total": profile.get(
                "messagesTotal",
                0
            ),
            "threads_total": profile.get(
                "threadsTotal",
                0
            ),
        }

    except Exception as error:

        print(
            "GMAIL CONNECT ERROR:",
            str(error)
        )

        # Gmail is not connected.
        # Tell frontend to start OAuth.

        try:

            flow = create_google_flow()

            authorization_url, state = (
                flow.authorization_url(
                    access_type="offline",
                    include_granted_scopes="true",
                    prompt="select_account consent",
                    state=str(
                        current_user.id
                    ),
                )
            )

            return {
                "success": True,
                "connected": False,
                "authorization_url": authorization_url,
            }

        except Exception as oauth_error:

            print(
                "GMAIL OAUTH ERROR:",
                str(oauth_error)
            )

            raise HTTPException(
                status_code=500,
                detail=str(oauth_error)
            )


# --------------------------------------------------
# GMAIL MESSAGES
# --------------------------------------------------

@router.get("/messages")
def get_messages(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):

    if limit < 1:
        limit = 1

    if limit > 100:
        limit = 100

    try:

        message_list = list_messages(
            user_id=current_user.id,
            max_results=limit
        )

        emails = []

        for item in message_list:

            message = get_message(
                user_id=current_user.id,
                message_id=item["id"]
            )

            payload = message.get(
                "payload",
                {}
            )

            headers = payload.get(
                "headers",
                []
            )

            email_data = {}

            for header in headers:

                name = header.get(
                    "name",
                    ""
                ).lower()

                value = header.get(
                    "value",
                    ""
                )

                email_data[name] = value

            body = extract_body(
                payload
            )

            attachments = extract_attachments(
                payload
            )

            emails.append({

                "id": message.get(
                    "id",
                    ""
                ),

                "sender": email_data.get(
                    "from",
                    ""
                ),

                "to": email_data.get(
                    "to",
                    ""
                ),

                "subject": email_data.get(
                    "subject",
                    "No subject"
                ),

                "date": email_data.get(
                    "date",
                    ""
                ),

                "body": body[:10000],

                "attachments": attachments,

                "analysis": {
                    "status": "pending"
                }

            })

        return {

            "success": True,

            "connected_user": {
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email
            },

            "count": len(emails),

            "emails": emails
        }

    except Exception as error:

        print(
            "GMAIL MESSAGES ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )




@router.post("/switch")
def switch_gmail(
    current_user: User = Depends(get_current_user)
):

    try:

        delete_user_gmail_token(
            current_user.id
        )

        return {
            "success": True,
            "connected": False,
            "message": (
                "Gmail connection removed. "
                "Connect Gmail again."
            )
        }

    except Exception as error:

        print(
            "GMAIL SWITCH ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )