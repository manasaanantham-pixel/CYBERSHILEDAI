import base64

from googleapiclient.discovery import build

from gmail.google_oauth import get_gmail_credentials


def get_gmail_service():

    credentials = get_gmail_credentials()

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


# =========================================================
# GMAIL PROFILE
# =========================================================

def get_profile():

    service = get_gmail_service()

    return service.users().getProfile(
        userId="me"
    ).execute()


# =========================================================
# LIST MESSAGES
# =========================================================

def list_messages(max_results=10):

    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    return response.get(
        "messages",
        []
    )


# =========================================================
# GET MESSAGE
# =========================================================

def get_message(message_id):

    service = get_gmail_service()

    return service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()


# =========================================================
# EXTRACT EMAIL BODY
# =========================================================

def extract_body(payload):

    body_text = ""

    if not payload:
        return body_text

    mime_type = payload.get(
        "mimeType",
        ""
    )

    body = payload.get(
        "body",
        {}
    )

    data = body.get(
        "data"
    )

    if data and mime_type in [
        "text/plain",
        "text/html"
    ]:

        try:

            decoded = base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

            body_text += decoded

        except Exception:
            pass


    for part in payload.get(
        "parts",
        []
    ):

        body_text += extract_body(
            part
        )


    return body_text


# =========================================================
# EXTRACT ATTACHMENTS
# =========================================================

def extract_attachments(payload):

    attachments = []

    if not payload:
        return attachments


    filename = payload.get(
        "filename",
        ""
    )

    body = payload.get(
        "body",
        {}
    )

    attachment_id = body.get(
        "attachmentId"
    )


    if filename and attachment_id:

        attachments.append({

            "filename": filename,

            "mime_type": payload.get(
                "mimeType",
                ""
            ),

            "attachment_id": attachment_id,

            "size": body.get(
                "size",
                0
            )

        })


    for part in payload.get(
        "parts",
        []
    ):

        attachments.extend(
            extract_attachments(part)
        )


    return attachments


# =========================================================
# DOWNLOAD ATTACHMENT
# =========================================================

def download_attachment(
    message_id,
    attachment_id
):

    service = get_gmail_service()

    attachment = (
        service.users()
        .messages()
        .attachments()
        .get(
            userId="me",
            messageId=message_id,
            id=attachment_id
        )
        .execute()
    )


    data = attachment.get(
        "data"
    )

    if not data:

        raise Exception(
            "Attachment data was not found"
        )


    return base64.urlsafe_b64decode(
        data
    )
    