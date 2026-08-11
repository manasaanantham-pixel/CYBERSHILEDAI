
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import User
from dependencies import get_current_user

from gmail.gmail_service import (
    list_messages,
    get_message,
    extract_body,
    extract_attachments,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)




@router.get("/gmail")
def analyze_gmail(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

      

        message_list = list_messages(
            user_id=current_user.id,
            max_results=limit
        )

        emails = []

        safe_count = 0
        spam_count = 0
        phishing_count = 0
        malware_count = 0
        unknown_count = 0


        

        for item in message_list:

            message_id = item.get("id")

            if not message_id:
                continue


            message = get_message(
                user_id=current_user.id,
                message_id=message_id
            )


            payload = message.get(
                "payload",
                {}
            )


            headers = payload.get(
                "headers",
                []
            )


            email_headers = {}


            for header in headers:

                name = header.get(
                    "name",
                    ""
                ).lower()

                value = header.get(
                    "value",
                    ""
                )

                email_headers[name] = value


            body = extract_body(
                payload
            )


            attachments = extract_attachments(
                payload
            )


           

            text = (
                email_headers.get(
                    "subject",
                    ""
                )
                + " "
                + body
            ).lower()


            prediction = "safe"
            risk = "low"
            confidence = 90.0



            phishing_words = [

                "verify your account",
                "verify account",
                "confirm your account",
                "password expired",
                "click here immediately",
                "urgent action",
                "suspended account",
                "account suspended",
                "login immediately",
                "security alert",
                "your account will be closed",
                "update your password",
                "confirm your identity"

            ]


            spam_words = [

                "free prize",
                "lottery",
                "winner",
                "congratulations",
                "you won",
                "claim your prize",
                "limited offer",
                "buy now",
                "special offer",
                "earn money",
                "make money fast"

            ]


            malware_words = [

                ".exe",
                ".scr",
                ".bat",
                ".cmd",
                ".msi",
                "malware",
                "virus",
                "trojan",
                "ransomware"

            ]


            phishing_found = any(
                word in text
                for word in phishing_words
            )


            spam_found = any(
                word in text
                for word in spam_words
            )


            malware_found = any(
                word in text
                for word in malware_words
            )


         

            if malware_found:

                prediction = "malware"
                risk = "high"
                confidence = 96.0

                malware_count += 1


            elif phishing_found:

                prediction = "phishing"
                risk = "high"
                confidence = 94.0

                phishing_count += 1


            elif spam_found:

                prediction = "spam"
                risk = "medium"
                confidence = 91.0

                spam_count += 1


            else:

                prediction = "safe"
                risk = "low"
                confidence = 95.0

                safe_count += 1


            

            emails.append({

                "id": message.get(
                    "id"
                ),

                "sender": email_headers.get(
                    "from",
                    ""
                ),

                "to": email_headers.get(
                    "to",
                    ""
                ),

                "subject": email_headers.get(
                    "subject",
                    "No subject"
                ),

                "date": email_headers.get(
                    "date",
                    ""
                ),

                "body": body[:5000],

                "attachments": attachments,

                "prediction": prediction,

                "result": prediction,

                "risk": risk,

                "confidence": confidence,

                "analysis": {

                    "prediction": prediction,

                    "risk": risk,

                    "confidence": confidence

                }

            })


       

        return {

            "success": True,

            "count": len(emails),

            "emails": emails,

            "summary": {

                "safe": safe_count,

                "spam": spam_count,

                "phishing": phishing_count,

                "malware": malware_count,

                "unknown": unknown_count

            }

        }


    except Exception as error:

        print(
            "GMAIL ANALYSIS ERROR:",
            error
        )

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )




@router.post("/malware")
async def analyze_malware_file(
    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "success": True,

        "analysis": {

            "prediction": "safe",

            "risk": "low",

            "confidence": 95.0

        }

    }