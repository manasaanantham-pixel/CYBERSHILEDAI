from fastapi import APIRouter, HTTPException

from gmail.gmail_service import (
    get_profile,
    list_messages,
    get_message,
    extract_body,
    extract_attachments
)


router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"]
)


# =========================================================
# CONNECT GMAIL
# =========================================================

@router.get("/connect")
def connect_gmail():

    try:

        profile = get_profile()

        return {
            "connected": True,

            "email": profile.get(
                "emailAddress"
            ),

            "messages_total": profile.get(
                "messagesTotal",
                0
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# GET EMAILS
# =========================================================

@router.get("/messages")
def get_messages(
    limit: int = 10
):

    try:

        message_list = list_messages(
            max_results=limit
        )

        emails = []

        for item in message_list:

            message = get_message(
                item["id"]
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
                    "id"
                ),

                "sender": email_data.get(
                    "from",
                    ""
                ),

                "subject": email_data.get(
                    "subject",
                    ""
                ),

                "date": email_data.get(
                    "date",
                    ""
                ),

                "body": body[:10000],

                "attachments": attachments
            })

        return {

            "count": len(emails),

            "emails": emails
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
        from fastapi import APIRouter, HTTPException

from gmail.gmail_service import (
    get_profile,
    list_messages,
    get_message,
    extract_body,
    extract_attachments
)


router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"]
)


# =========================================================
# CONNECT GMAIL
# =========================================================

@router.get("/connect")
def connect_gmail():

    try:

        profile = get_profile()

        return {
            "connected": True,

            "email": profile.get(
                "emailAddress"
            ),

            "messages_total": profile.get(
                "messagesTotal",
                0
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# GET EMAILS
# =========================================================

@router.get("/messages")
def get_messages(
    limit: int = 10
):

    try:

        message_list = list_messages(
            max_results=limit
        )

        emails = []

        for item in message_list:

            message = get_message(
                item["id"]
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
                    "id"
                ),

                "sender": email_data.get(
                    "from",
                    ""
                ),

                "subject": email_data.get(
                    "subject",
                    ""
                ),

                "date": email_data.get(
                    "date",
                    ""
                ),

                "body": body[:10000],

                "attachments": attachments
            })

        return {

            "count": len(emails),

            "emails": emails
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )