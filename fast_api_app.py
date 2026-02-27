from fastapi import FastAPI, Response, HTTPException
from firewall.validator import validate_and_clean
from core.models import Event, Incident
from core.planner import run_investigation
import json
import os
from uuid import uuid4
from utility.logger import get_logger
import datetime
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

logger = get_logger()

EVENTS_FILE = "data/events.json"

app = FastAPI(title="AIRE Secure Event Pipeline API")

# Prometheus metrics
events_processed = Counter("events_processed_total", "Total events processed")
incidents_created = Counter("incidents_created_total", "Total incidents created")
auto_responses = Counter("auto_responses_total", "Total automated responses executed")
investigation_time = Histogram("investigation_duration_seconds", "Time spent investigating")

# Mount static files and set up templates from ui/ directory
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

def append_to_json_file(filename, obj):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
    with open(filename, "r+") as f:
        data = json.load(f)
        data.append(obj)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

@app.post("/ingest", response_model=Incident)
def ingest_event(event: Event):
    import traceback
    trace_id = str(uuid4())
    try:
        # SECURITY: Validate and sanitize the incoming event using firewall
        cleaned_event, error = validate_and_clean(event.dict())
        if error:
            logger.warning(
                "Event rejected by firewall validation",
                extra={
                    "trace_id": trace_id,
                    "stage": "firewall_validation",
                    "error": error,
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
                }
            )
            raise HTTPException(status_code=400, detail=f"Event validation failed: {error}")

        logger.info(
            "Event ingested",
            extra={
                "trace_id": trace_id,
                "event_id": cleaned_event.get("event_id", "unknown"),
                "stage": "event_ingestion",
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "details": cleaned_event
            }
        )
        events_processed.inc()
        append_to_json_file(EVENTS_FILE, cleaned_event)
        # Convert cleaned_event back to Event model for downstream pipeline
        event_obj = Event(**cleaned_event)
        with investigation_time.time():
            incident = run_investigation(event_obj, trace_id=trace_id)
        # Also store incident in data/incidents.json if it exists
        if incident:
            incidents_created.inc()
            if getattr(incident, 'auto_response_executed', False):
                auto_responses.inc()
            append_to_json_file("data/incidents.json", incident.dict())
            return incident
        return {"message": "Event logged. Not suspicious."}
    except Exception as e:
        tb_str = traceback.format_exc()
        logger.error(f"Error in /ingest endpoint: {e}\n{tb_str}", extra={"trace_id": trace_id, "stage": "error"})
        return Response(
            content=f"Internal Server Error.\n{tb_str}",
            status_code=500,
            media_type="text/plain"
        )

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/dashboard")
def dashboard(request: Request):
    # Load real data from files
    try:
        with open("data/events.json") as f:
            events = json.load(f)
    except Exception:
        events = []
    try:
        with open("data/incidents.json") as f:
            incidents = json.load(f)
    except Exception:
        incidents = []
    total_events = len(events)
    high_count = sum(1 for i in incidents if i.get("severity") == "High")
    auto_responses = sum(1 for i in incidents if i.get("auto_response_executed"))
    # Calculate average investigation time if available
    times = [i.get("investigation_time", 0) for i in incidents if i.get("investigation_time")]
    avg_investigation_time = round(sum(times) / len(times), 2) if times else 0
    # Events by type
    event_types = [e.get("event_type", "Unknown") for e in events]
    event_type_labels = list(sorted(set(event_types)))
    event_type_data = [event_types.count(l) for l in event_type_labels]
    # Incidents by severity
    severities = [i.get("severity", "Unknown") for i in incidents]
    severity_labels = ["High", "Medium", "Low", "Unknown"]
    severity_data = [severities.count(l) for l in severity_labels]
    # Investigation times
    investigation_times = times
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_events": total_events,
        "high_count": high_count,
        "auto_responses": auto_responses,
        "avg_investigation_time": avg_investigation_time,
        "event_type_labels": event_type_labels,
        "event_type_data": event_type_data,
        "severity_labels": severity_labels,
        "severity_data": severity_data,
        "investigation_times": investigation_times
    })

@app.get("/incidents")
def get_incidents(request: Request):
    # Load incidents from file
    try:
        with open("data/incidents.json") as f:
            incidents = json.load(f)
    except Exception:
        incidents = []
    return templates.TemplateResponse("incidents.html", {"request": request, "incidents": incidents})

@app.get("/incidents/{incident_id}")
def incident_detail(incident_id: str, request: Request):
    try:
        with open("data/incidents.json") as f:
            incidents = json.load(f)
    except Exception:
        incidents = []
    incident = next((i for i in incidents if i.get("incident_id") == incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    # Only show fields from incidents.json
    # For event_data, load from events.json if event_id exists
    event_data = {}
    event_id = incident.get("event_id")
    if event_id:
        try:
            with open("data/events.json") as f:
                events = json.load(f)
            event_data = next((e for e in events if e.get("event_id") == event_id), {})
        except Exception:
            event_data = {}
    # Defensive: fill in explainability fields if missing
    incident.setdefault("risk_breakdown", ["No breakdown available"])
    incident.setdefault("policy_references", ["No references"])
    incident.setdefault("trace_timeline", ["No trace available"])
    # Only pass the event_data from events.json
    return templates.TemplateResponse("incident_detail.html", {"request": request, "incident": incident, "event_data": event_data})

@app.get("/metrics")
def metrics_page(request: Request):
    # Example: count incidents by severity
    try:
        with open("data/incidents.json") as f:
            incidents = json.load(f)
    except Exception:
        incidents = []
    severities = [i.get("severity", "Unknown") for i in incidents]
    labels = ["High", "Medium", "Low"]
    data = [severities.count(l) for l in labels]
    return templates.TemplateResponse("metrics.html", {"request": request, "labels": labels, "data": data})

@app.post("/approve")
def approve(incident_id: str):
    # Implement approval logic here
    # For now, just update status in file
    try:
        with open("data/incidents.json", "r+") as f:
            incidents = json.load(f)
            for i in incidents:
                if i.get("incident_id") == incident_id:
                    i["status"] = "RESPONDED"
            f.seek(0)
            json.dump(incidents, f, indent=2)
            f.truncate()
    except Exception:
        pass
    return {"status": "approved"}

@app.post("/reject")
def reject(incident_id: str):
    # Implement rejection logic here
    try:
        with open("data/incidents.json", "r+") as f:
            incidents = json.load(f)
            for i in incidents:
                if i.get("incident_id") == incident_id:
                    i["status"] = "REJECTED"
            f.seek(0)
            json.dump(incidents, f, indent=2)
            f.truncate()
    except Exception:
        pass
    return {"status": "rejected"}

# Add this endpoint to serve the latest logs as JSON
@app.get("/logs")
def get_logs():
    # Adjust the log file path as needed
    log_file = "logs/aire.log"
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
        # Return the last 100 log lines (or fewer)
        return {"logs": lines[-100:]}
    except Exception:
        return {"logs": ["No logs found."]}
