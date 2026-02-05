import re

def extract_scammer_info(text: str):
    upi_pattern = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
    phone_pattern = r"\b[6-9]\d{9}\b"
    bank_pattern = r"\b\d{9,18}\b"
    link_pattern = r"https?://\S+"

    upi_ids = re.findall(upi_pattern, text)
    phone_numbers = re.findall(phone_pattern, text)
    bank_accounts = re.findall(bank_pattern, text)
    links = re.findall(link_pattern, text)

    return {
        "upi_ids": list(set(upi_ids)),
        "phone_numbers": list(set(phone_numbers)),
        "bank_accounts": list(set(bank_accounts)),
        "links": list(set(links)),
    }