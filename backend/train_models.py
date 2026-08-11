import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# =========================================================
# TRAINING DATA
# =========================================================

data = [
    # ---------------- SPAM ----------------
    ("Congratulations! You won a free lottery prize. Claim now!", "spam"),
    ("You have won $1,000,000. Click here to claim your reward.", "spam"),
    ("Limited time offer! Buy now and get 90% discount.", "spam"),
    ("You are selected for a special cash reward.", "spam"),
    ("Earn money quickly from home. Contact us today.", "spam"),
    ("Free gift waiting for you. Click the link now.", "spam"),

    # ---------------- PHISHING ----------------
    ("Your account has been suspended. Verify your password immediately.", "phishing"),
    ("Urgent security alert. Click here to confirm your account.", "phishing"),
    ("Your bank account will be closed unless you verify your information.", "phishing"),
    ("We detected unusual activity. Login immediately to secure your account.", "phishing"),
    ("Confirm your username and password to prevent account termination.", "phishing"),
    ("Your payment failed. Update your banking information now.", "phishing"),

    # ---------------- SAFE ----------------
    ("Hi, are we still meeting tomorrow at 10 AM?", "safe"),
    ("Please find the meeting notes attached.", "safe"),
    ("Thank you for your email. I will get back to you soon.", "safe"),
    ("Your appointment is confirmed for Friday.", "safe"),
    ("Here is the project report we discussed.", "safe"),
    ("The team meeting has been moved to Monday.", "safe"),
]


df = pd.DataFrame(
    data,
    columns=["text", "label"]
)




model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])




model.fit(
    df["text"],
    df["label"]
)




os.makedirs("ml", exist_ok=True)

joblib.dump(
    model,
    "ml/email_security_model.pkl"
)

print()
print("======================================")
print(" CyberShield AI ML MODEL")
print("======================================")
print("Training completed successfully.")
print()
print("Model saved:")
print("ml/email_security_model.pkl")
print()
