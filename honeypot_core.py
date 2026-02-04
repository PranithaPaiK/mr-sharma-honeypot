# honeypot_core.py
# =======================
# SCAM KEYWORD DETECTION
# =======================

GENERIC_SCAM_KEYWORDS = [
    "otp", "kyc", "account blocked", "verify",
    "refund", "upi", "collect request",
    "click here", "bit.ly", "tinyurl",
    "password", "cvv", "pin"
]

MEDICAL_WORDS = [
    "hospital", "hospitalized", "icu",
    "surgery", "accident", "critical"
]

FAMILY_WORDS = [
    "son", "daughter", "child",
    "father", "mother", "husband", "wife"
]

MONEY_WORDS = [
    "money", "payment", "funds",
    "transfer", "hospital bill"
]

URGENCY_WORDS = [
    "urgent", "immediately", "now",
    "no time", "right now"
]

def calculate_scam_risk(message: str) -> dict:
    msg = message.lower()
    score = 0
    reasons = []

    if any(w in msg for w in GENERIC_SCAM_KEYWORDS):
        score += 3
        reasons.append("generic scam pattern")

    if any(w in msg for w in MEDICAL_WORDS):
        score += 3
        reasons.append("medical emergency")

    if any(w in msg for w in FAMILY_WORDS):
        score += 2
        reasons.append("family impersonation")

    if any(w in msg for w in MONEY_WORDS):
        score += 3
        reasons.append("money request")

    if any(w in msg for w in URGENCY_WORDS):
        score += 2
        reasons.append("urgency pressure")

    risk = "LOW"
    if score >= 7:
        risk = "HIGH"
    elif score >= 4:
        risk = "MEDIUM"

    return {
        "risk": risk,
        "score": score,
        "reasons": reasons
    }