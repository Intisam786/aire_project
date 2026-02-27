from core.detection import run_detection
from core.risk_engine import calculate_risk
from core.response_engine import simulate_disable_account
from core.storage import append_incident
from core.models import Incident
from datetime import datetime
from core.team_pipeline import run_team_investigation
import uuid
from utility.logger import get_logger
logger = get_logger()

def run_investigation(event, trace_id=None):
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    # Step 1: Detection
    suspicious, findings, risk_score, baseline = run_detection(event, trace_id=trace_id)
    logger.info(
        "Detection decision",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "detection",
            "agent": "DetectionAgent",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "suspicious": suspicious,
            "risk_score": risk_score
        }
    )
    # Only proceed if risk_score >= threshold
    RISK_THRESHOLD = 30
    if not suspicious or risk_score < RISK_THRESHOLD:
        return None

    # Set confidence (static or dynamic as needed)
    confidence = 88  # Placeholder, can be replaced with dynamic calculation

    # Step 2: Deep investigation via team-based group chat (AutoGen Team)
    # Pass baseline to CriticAgent via event context or as needed
    result = run_team_investigation(event, trace_id=trace_id, baseline=baseline)
    logger.info(
        "Planner and agent outputs",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "investigation",
            "agent": "TeamInvestigation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_responses": str(result),
            "confidence": confidence
        }
    )

    # Step 4: Decision engine
    if risk_score > 85:
        auto_response = simulate_disable_account(event.user, trace_id=trace_id)
        severity = "High"
    elif risk_score > 50:
        auto_response = False
        severity = "Medium"
    else:
        auto_response = False
        severity = "Low"
    logger.info(
        "Response decision",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "response_decision",
            "agent": "ResponseAgent",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": severity,
            "auto_response": auto_response
        }
    )
    # Step 5: Build incident report
    incident = Incident(
        incident_id=f"I{uuid.uuid4().hex[:6].upper()}",
        event_id=event.event_id,
        severity=severity,
        risk_score=risk_score,
        confidence=confidence,
        findings=findings,
        recommended_actions=["Disable account", "Revoke role"] if severity=="High" else ["Review activity"],
        auto_response_executed=auto_response
    )
    append_incident(incident.dict())
    logger.info(
        "Incident stored",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "incident_storage",
            "agent": "ResponseAgent",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "incident_id": incident.incident_id
        }
    )
    return incident
