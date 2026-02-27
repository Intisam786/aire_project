INJECTION_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "act as",
    "execute this"
]

def detect_prompt_injection(text: str) -> bool:
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in INJECTION_PATTERNS)
