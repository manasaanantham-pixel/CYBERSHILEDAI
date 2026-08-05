import base64


def decode_body(data):

    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(
            data + "=="
        )

        return decoded.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:
        return ""


def get_headers(headers):

    result = {}

    for header in headers:

        name = header.get("name", "").lower()
        value = header.get("value", "")

        result[name] = value

    return result


def parse_parts(parts):

    text = ""
    attachments = []

    for part in parts:

        mime_type = part.get(
            "mimeType",
            ""
        )

        filename = part.get(
            "filename",
            ""
        )

        body = part.get(
            "body",
            {}
        )

        # Attachment
        if filename:

            attachments.append({
                "filename": filename,
                "mime_type": mime_type,
                "attachment_id": body.get(
                    "attachmentId"
                ),
                "size": body.get(
                    "size",
                    0
                )
            })

        # Text
        if mime_type == "text/plain":

            data = body.get("data")

            if data:
                text += decode_body(data)

        # HTML
        elif mime_type == "text/html":

            data = body.get("data")

            if data and not text:

                text += decode_body(data)

        # Nested multipart
        nested_parts = part.get("parts", [])

        if nested_parts:

            nested_text, nested_attachments = parse_parts(
                nested_parts
            )

            text += nested_text
            attachments.extend(
                nested_attachments
            )

    return text, attachments


def parse_email(message):

    payload = message.get(
        "payload",
        {}
    )

    headers = get_headers(
        payload.get(
            "headers",
            []
        )
    )

    body = ""

    attachments = []

    parts = payload.get(
        "parts",
        []
    )

    if parts:

        body, attachments = parse_parts(parts)

    else:

        data = payload.get(
            "body",
            {}
        ).get("data")

        body = decode_body(data)

    return {

        "id": message.get("id"),

        "thread_id": message.get(
            "threadId"
        ),

        "sender": headers.get(
            "from",
            ""
        ),

        "to": headers.get(
            "to",
            ""
        ),

        "subject": headers.get(
            "subject",
            ""
        ),

        "date": headers.get(
            "date",
            ""
        ),

        "body": body,

        "attachments": attachments
    }
    