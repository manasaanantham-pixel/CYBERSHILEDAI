from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ml.predictor import analyze_email

from gmail.gmail_service import (
    list_messages,
    get_message,
    extract_body,
    extract_attachments
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/analysis",
    tags=["Email Analysis"]
)


# =========================================================
# MANUAL EMAIL ANALYSIS
# =========================================================

class EmailAnalysisRequest(BaseModel):
    text: str


@router.post("/email")
def analyze_email_api(
    email: EmailAnalysisRequest
):

    try:

        result = analyze_email(
            email.text
        )

        return {
            "success": True,
            "analysis": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# GMAIL EMAIL ANALYSIS
# =========================================================

@router.get("/gmail")
def analyze_gmail_messages(
    limit: int = 10
):

    try:

        # -------------------------------------------------
        # GET GMAIL MESSAGE IDS
        # -------------------------------------------------

        message_list = list_messages(
            max_results=limit
        )

        analyzed_emails = []


        # -------------------------------------------------
        # PROCESS EACH EMAIL
        # -------------------------------------------------

        for message_info in message_list:

            message_id = message_info.get(
                "id"
            )

            if not message_id:
                continue


            # -------------------------------------------------
            # GET FULL MESSAGE
            # -------------------------------------------------

            message = get_message(
                message_id
            )

            payload = message.get(
                "payload",
                {}
            )


            # -------------------------------------------------
            # EMAIL HEADERS
            # -------------------------------------------------

            headers = payload.get(
                "headers",
                []
            )

            sender = ""
            subject = ""
            date = ""

            for header in headers:

                name = header.get(
                    "name",
                    ""
                ).lower()

                value = header.get(
                    "value",
                    ""
                )

                if name == "from":

                    sender = value

                elif name == "subject":

                    subject = value

                elif name == "date":

                    date = value


            # -------------------------------------------------
            # EMAIL BODY
            # -------------------------------------------------

            body = extract_body(
                payload
            )


            # -------------------------------------------------
            # ATTACHMENTS
            # -------------------------------------------------

            attachments = extract_attachments(
                payload
            )


            # -------------------------------------------------
            # AI EMAIL ANALYSIS
            #
            # IMPORTANT:
            # Analyze sender + subject + body
            # -------------------------------------------------

            result = analyze_email(

                body,

                subject=subject,

                sender=sender

            )


            # -------------------------------------------------
            # FINAL EMAIL RESULT
            # -------------------------------------------------

            analyzed_emails.append({

                "id": message_id,

                "sender": sender,

                "subject": subject,

                "date": date,

                "prediction": result.get(
                    "prediction",
                    "unknown"
                ),

                "risk": result.get(
                    "risk",
                    "unknown"
                ),

                "confidence": result.get(
                    "confidence",
                    0
                ),

                "reasons": result.get(
                    "reasons",
                    []
                ),

                "attachments": attachments

            })


        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        safe_count = 0
        spam_count = 0
        phishing_count = 0
        malware_count = 0
        unknown_count = 0

        for email in analyzed_emails:

            prediction = email.get(
                "prediction"
            )

            if prediction == "safe":

                safe_count += 1

            elif prediction == "spam":

                spam_count += 1

            elif prediction == "phishing":

                phishing_count += 1

            elif prediction == "malware":

                malware_count += 1

            else:

                unknown_count += 1


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "success": True,

            "count": len(
                analyzed_emails
            ),

            "summary": {

                "safe": safe_count,

                "spam": spam_count,

                "phishing": phishing_count,

                "malware": malware_count,

                "unknown": unknown_count

            },

            "emails": analyzed_emails

        }


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )
        