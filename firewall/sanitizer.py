import re

def sanitize_text(text: str) -> str:
    if text is None:
        return ""
    text = re.sub(r"<.*?>", "", text)
    text = text[:2000]
    return text
