
from utility.logger import get_logger
logger = get_logger()


import json
import os

def load_baselines():
    baseline_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "baseline_profiles.json")
    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_user_baseline(user, baselines):
    uname = user.lower()
    if "admin" in uname:
        return baselines.get("admin_account", {})
    if "service" in uname:
        return baselines.get("service_account", {})
    if "contractor" in uname:
        return baselines.get("contractor", {})
    return baselines.get("employee", {})

def run_detection(event, trace_id=None):
    if trace_id is None:
        trace_id = "N/A"
    baselines = load_baselines()
    baseline = get_user_baseline(getattr(event, 'user', ''), baselines)
    findings = []
    risk_score = 0
    # Example: location anomaly
    if getattr(event, 'location', None) and baseline.get("common_locations"):
        if event.location not in baseline["common_locations"]:
            findings.append("Login from unusual location")
            risk_score += 20
    # Example: role anomaly
    if getattr(event, 'action', None) and baseline.get("normal_roles"):
        if event.action not in baseline["normal_roles"]:
            findings.append("Unusual role assignment")
            risk_score += 15
    # Example: time anomaly (not implemented, but could be added)
    # Example: approval ticket
    if hasattr(event, 'approved_ticket') and not event.approved_ticket:
        findings.append("No approval ticket")
        risk_score += 10
    suspicious = risk_score > 0
    logger.info(
        "Detection logic executed",
        extra={
            "trace_id": trace_id,
            "event_id": getattr(event, 'event_id', None),
            "stage": "detection_logic",
            "findings": findings,
            "risk_score": risk_score,
            "suspicious": suspicious,
            "baseline": baseline
        }
    )
    return suspicious, findings, risk_score, baseline
