from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    event_id: str
    timestamp: str
    source: str  # IAM / Cloud
    event_type: str
    user: str
    ip_address: str
    location: str
    approved_ticket: bool = False

class Incident(BaseModel):
    incident_id: str
    event_id: str
    severity: str
    risk_score: int
    confidence: int
    findings: List[str]
    recommended_actions: List[str]
    auto_response_executed: bool
