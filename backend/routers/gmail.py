
from fastapi import APIRouter, Depends, HTTPException
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

router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"]
)




@router.get("/status")
def gmail_status(
    current_user: User = Depends(get_current_user)
):
    try:
        profile = get_profile(current_user.id)

        return {
            "success": True,
            "connected": True,
            "email": profile.get("emailAddress", ""),
            "messages_total": profile.get("messagesTotal", 0),
            "threads_total": profile.get("threadsTotal", 0),
        }

    except Exception:
        return {
            "success": True,
            "connected": False,
            "email": "",
            "messages_total": 0,
            "threads_total": 0,
        }




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
            )
        }

    except Exception as error:

        error_message = str(error)

        # Gmail account is not connected yet
        if (
            "token" in error_message.lower()
            or "credential" in error_message.lower()
            or "401" in error_message
            or "unauthorized" in error_message.lower()
        ):
            raise HTTPException(
                status_code=401,
                detail="Gmail is not connected. Please connect your Google account."
            )

        raise HTTPException(
            status_code=500,
            detail=error_message
        )




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

        error_message = str(error)

        if (
            "401" in error_message
            or "unauthorized" in error_message.lower()
            or "token" in error_message.lower()
            or "credential" in error_message.lower()
        ):
            raise HTTPException(
                status_code=401,
                detail="Gmail authorization expired. Please connect Gmail again."
            )

        raise HTTPException(
            status_code=500,
            detail=error_message
        )




@router.post("/switch")
def switch_gmail(
    current_user: User = Depends(get_current_user)
):

    try:

        from gmail.google_oauth import (
            delete_user_gmail_token
        )

        delete_user_gmail_token(
            current_user.id
        )

        return {
            "success": True,
            "connected": False,
            "message": "Gmail connection removed. Connect Gmail again."
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
