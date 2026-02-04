import re

def extract_scammer_info(message: str) -> dict:
    """Extract UPI IDs, bank accounts, phone numbers, and links from message."""
    
    upi_pattern = r'[a-zA-Z0-9._-]+@[a-zA-Z]{2,}'
    bank_pattern = r'\b\d{9,18}\b'
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
    
    return {
        "upi_ids": list(set(re.findall(upi_pattern, message))),
        "bank_accounts": list(set(re.findall(bank_pattern, message))),
        "links": list(set(re.findall(url_pattern, message, re.IGNORECASE))),
        "phone_numbers": list(set(re.findall(phone_pattern, message)))
    }