from firewall.schema import LogEvent
from firewall.injection_detector import detect_prompt_injection
from firewall.sanitizer import sanitize_text
from pydantic import ValidationError

def validate_and_clean(data):
    # Only pass the fields required by LogEvent

    log_fields = {}
    for field in ["timestamp", "user", "action", "ip", "resource"]:
        if field in data:
            log_fields[field] = data[field]

    # DEBUG: Log what is being passed to LogEvent
    import sys
    print(f"[DEBUG] LogEvent fields: {log_fields}", file=sys.stderr)

    try:
        log = LogEvent(**log_fields)
    except ValidationError as ve:
        print(f"[DEBUG] ValidationError: {ve}", file=sys.stderr)
        return None, f"Schema validation failed: {ve}"

    if detect_prompt_injection(log_fields.get("action", "")):
        return None, "Prompt injection detected"


    if log.action is not None:
        log.action = sanitize_text(log.action)

    # Return the original event dict (with all fields) for downstream pipeline, but validated
    return data, None
