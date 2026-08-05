import os
import re
import joblib
import pandas as pd


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ML_DIR = os.path.join(BASE_DIR, "ml")

EMAIL_MODEL_PATH = os.path.join(
    ML_DIR, "email_security_model.pkl"
)

MALWARE_MODEL_PATH = os.path.join(
    ML_DIR, "malware_model.pkl"
)

MALWARE_FEATURES_PATH = os.path.join(
    ML_DIR, "malware_features.pkl"
)


# =========================================================
# LOAD MODELS
# =========================================================

print("Loading CyberShield AI models...")

email_model = None
malware_model = None
malware_features = None

try:
    if os.path.exists(EMAIL_MODEL_PATH):
        email_model = joblib.load(EMAIL_MODEL_PATH)
        print("Email security model loaded successfully")
    else:
        print("WARNING: Email model not found")

except Exception as e:
    print("ERROR loading email model:", e)


try:
    if os.path.exists(MALWARE_MODEL_PATH):
        malware_model = joblib.load(MALWARE_MODEL_PATH)
        print("Malware model loaded successfully")
    else:
        print("WARNING: Malware model not found")

except Exception as e:
    print("ERROR loading malware model:", e)


try:
    if os.path.exists(MALWARE_FEATURES_PATH):
        malware_features = joblib.load(MALWARE_FEATURES_PATH)
        print("Malware features loaded successfully")
    else:
        print("WARNING: Malware features not found")

except Exception as e:
    print("ERROR loading malware features:", e)


print("CyberShield AI models ready.")


# =========================================================
# RISK CALCULATION
# =========================================================

def calculate_email_risk(prediction, confidence):

    prediction = str(prediction).lower()

    # Phishing is inherently dangerous.
    if prediction == "phishing":

        if confidence >= 70:
            return "critical"

        return "high"

    # Malware in an email is also dangerous.
    if prediction == "malware":

        if confidence >= 70:
            return "critical"

        return "high"

    # Spam
    if prediction == "spam":

        if confidence >= 80:
            return "high"

        if confidence >= 50:
            return "medium"

        return "low"

    # Safe
    if prediction == "safe":
        return "low"

    return "unknown"


# =========================================================
# SECURITY REASONS
# =========================================================

def get_security_reasons(text, prediction):

    text_lower = str(text).lower()

    reasons = []

    phishing_keywords = [
        "verify your account",
        "verify account",
        "confirm your account",
        "password",
        "login",
        "sign in",
        "security alert",
        "account suspended",
        "account locked",
        "click here",
        "urgent",
        "immediately",
        "verify now"
    ]

    spam_keywords = [
        "free",
        "winner",
        "won",
        "lottery",
        "prize",
        "cash",
        "discount",
        "offer",
        "congratulations"
    ]

    suspicious_links = [
        "http://",
        "bit.ly/",
        "tinyurl.com/",
        "t.co/"
    ]

    if prediction == "phishing":

        for keyword in phishing_keywords:

            if keyword in text_lower:

                reasons.append(
                    f"Suspicious phrase detected: '{keyword}'"
                )

                if len(reasons) >= 3:
                    break

        for link in suspicious_links:

            if link in text_lower:

                reasons.append(
                    "Potentially suspicious link detected"
                )

                break

    elif prediction == "spam":

        for keyword in spam_keywords:

            if keyword in text_lower:

                reasons.append(
                    f"Spam indicator detected: '{keyword}'"
                )

                if len(reasons) >= 3:
                    break

    if not reasons:

        if prediction == "safe":

            reasons.append(
                "No major suspicious indicators detected"
            )

        else:

            reasons.append(
                "AI model detected potentially suspicious content"
            )

    return reasons


# =========================================================
# EMAIL ANALYSIS
# =========================================================

def analyze_email(
    text: str,
    subject: str = "",
    sender: str = ""
):

    # Combine all available email information
    combined_text = " ".join([
        str(sender or ""),
        str(subject or ""),
        str(text or "")
    ]).strip()

    if not combined_text:

        return {
            "prediction": "safe",
            "risk": "low",
            "confidence": 0,
            "reasons": [
                "No email content available for analysis"
            ]
        }

    if email_model is None:

        return {
            "prediction": "unknown",
            "risk": "unknown",
            "confidence": 0,
            "reasons": [],
            "error": "Email security model not found"
        }

    try:

        # -------------------------------------------------
        # AI MODEL PREDICTION
        # -------------------------------------------------

        prediction = email_model.predict(
            [combined_text]
        )[0]

        prediction = str(
            prediction
        ).lower().strip()


        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = 0.0

        if hasattr(
            email_model,
            "predict_proba"
        ):

            probabilities = email_model.predict_proba(
                [combined_text]
            )[0]

            confidence = float(
                max(probabilities) * 100
            )


        # -------------------------------------------------
        # NORMALIZE LABEL
        # -------------------------------------------------

        if prediction in [
            "benign",
            "ham",
            "normal",
            "legitimate"
        ]:

            prediction = "safe"

        elif prediction in [
            "phishing",
            "phish"
        ]:

            prediction = "phishing"

        elif prediction in [
            "spam"
        ]:

            prediction = "spam"

        elif prediction in [
            "malware"
        ]:

            prediction = "malware"

        elif prediction not in [
            "safe",
            "spam",
            "phishing",
            "malware"
        ]:

            prediction = "safe"


        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        risk = calculate_email_risk(
            prediction,
            confidence
        )


        # -------------------------------------------------
        # REASONS
        # -------------------------------------------------

        reasons = get_security_reasons(
            combined_text,
            prediction
        )


        return {

            "prediction": prediction,

            "risk": risk,

            "confidence": round(
                confidence,
                2
            ),

            "reasons": reasons

        }


    except Exception as error:

        return {

            "prediction": "unknown",

            "risk": "unknown",

            "confidence": 0,

            "reasons": [],

            "error": str(error)

        }


# =========================================================
# MALWARE ANALYSIS
# =========================================================

def predict_malware(file_path: str):

    if malware_model is None:

        return {

            "prediction": "unknown",

            "risk": "unknown",

            "confidence": 0,

            "error": "Malware model not found"

        }

    try:

        from ml.pe_features import extract_pe_features

        # Extract PE features
        features = extract_pe_features(
            file_path
        )

        # Convert to DataFrame
        if isinstance(features, dict):

            data = pd.DataFrame(
                [features]
            )

        else:

            data = pd.DataFrame(
                [features]
            )

        # -------------------------------------------------
        # MATCH TRAINING FEATURES
        # -------------------------------------------------

        if malware_features is not None:

            if isinstance(
                malware_features,
                (list, tuple)
            ):

                for feature in malware_features:

                    if feature not in data.columns:

                        data[feature] = 0

                data = data[
                    list(malware_features)
                ]


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = malware_model.predict(
            data
        )[0]


        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = 0.0

        if hasattr(
            malware_model,
            "predict_proba"
        ):

            probabilities = malware_model.predict_proba(
                data
            )[0]

            confidence = float(
                max(probabilities) * 100
            )


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if int(prediction) == 1:

            result = "malware"
            risk = "critical"

        else:

            result = "safe"
            risk = "low"


        return {

            "prediction": result,

            "risk": risk,

            "confidence": round(
                confidence,
                2
            )

        }


    except Exception as error:

        return {

            "prediction": "unknown",

            "risk": "unknown",

            "confidence": 0,

            "error": str(error)

        }
        