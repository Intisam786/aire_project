
from utility.logger import get_logger
logger = get_logger()

def calculate_risk(signals, trace_id=None):
    if trace_id is None:
        trace_id = "N/A"
    score = 0
    # Baseline-aware scoring additions
    import os, json
    baseline_path = os.path.join(os.path.dirname(__file__), "data", "baseline_profiles.json")
    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            baselines = json.load(f)
    except Exception:
        baselines = {}

    # Helper: map user/account to baseline profile
    def get_baseline(user):
        # Simple mapping: if user matches a baseline key, use it; else default to 'employee'
        if user in baselines:
            return baselines[user]
        # Heuristic: admin/service/contractor in username
        uname = user.lower()
        if "admin" in uname:
            return baselines.get("admin_account", {})
        if "service" in uname:
            return baselines.get("service_account", {})
        if "contractor" in uname:
            return baselines.get("contractor", {})
        return baselines.get("employee", {})

    # Find user in signals if present
    user = None
    for s in signals:
        if isinstance(s, dict) and "user" in s:
            user = s["user"]
        elif isinstance(s, str) and "user" in s:
            user = s.split(":")[-1].strip()
    # Fallback: try to get from signals context
    if not user and signals:
        # If signals is from detection, may have event context
        import inspect
        frame = inspect.currentframe().f_back
        event = frame.f_locals.get("event", None)
        if event and hasattr(event, "user"):
            user = getattr(event, "user")

    baseline = get_baseline(user or "employee")
    # Contextual scoring
    # Assume signals may include event context
    event = None
    import inspect
    frame = inspect.currentframe().f_back
    if "event" in frame.f_locals:
        event = frame.f_locals["event"]

    findings = list(signals)
    # Location
    if event and hasattr(event, "location") and baseline.get("common_locations"):
        if event.location not in baseline["common_locations"]:
            score += 25
            findings.append(f"Location {event.location} not in baseline {baseline['common_locations']}")
        else:
            score -= 15
            findings.append(f"Location {event.location} matches baseline")
    # Role
    if event and hasattr(event, "event_type") and hasattr(event, "user"):
        # Try to get role from event_type or user
        role = getattr(event, "role", None)
        if not role and hasattr(event, "event_type") and "role" in event.event_type.lower():
            # crude guess: event_type like 'RoleAssigned' => role assignment
            role = "SecurityOperator" if "admin" in event.user.lower() else "User"
        if role and baseline.get("normal_roles"):
            if role not in baseline["normal_roles"]:
                score += 30
                findings.append(f"Role {role} not in baseline {baseline['normal_roles']}")
            else:
                score -= 10
                findings.append(f"Role {role} matches baseline")
    # Time (hour)
    if event and hasattr(event, "timestamp") and baseline.get("normal_hours"):
        import re
        from datetime import datetime
        try:
            hour = int(datetime.fromisoformat(event.timestamp.replace("Z", "")).hour)
            hours = baseline["normal_hours"].split("-")
            start, end = int(hours[0]), int(hours[1])
            if not (start <= hour <= end):
                score += 20
                findings.append(f"Hour {hour} outside baseline {baseline['normal_hours']}")
            else:
                score -= 5
                findings.append(f"Hour {hour} matches baseline")
        except Exception:
            pass

    # Classic signals
    if "Privileged role assigned" in signals:
        score += 50
    if "Login from unusual location" in signals:
        score += 30
    if "No approval ticket" in signals:
        score += 40
    score = min(max(score, 0), 100)
    logger.info(
        "Risk scoring logic executed",
        extra={
            "trace_id": trace_id,
            "stage": "risk_scoring_logic",
            "signals": signals,
            "risk_score": score,
            "baseline": baseline,
            "baseline_findings": findings
        }
    )
    return score
