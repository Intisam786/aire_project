from utility.logger import get_logger
import uuid
logger = get_logger()
# Example: Log app start
logger.info("App started", extra={"stage": "startup", "trace_id": str(uuid.uuid4())})
# Example: Log input validation
def validate_input(input_data, user=None):
	if not input_data or not isinstance(input_data, dict):
		logger.error("Input validation failed", extra={"stage": "input_validation", "input": input_data, "user": user, "trace_id": str(uuid.uuid4())})
		return False
	# Add OWASP LLM/Agent Top 10 checks here
	return True
# Example: Log agent action
def log_agent_action(agent_name, action, event_id, trace_id):
	logger.info(f"Agent action: {action}", extra={"stage": "agent_action", "agent": agent_name, "event_id": event_id, "trace_id": trace_id})
# Example: Log error
def log_error(error_msg, event_id=None, trace_id=None):
	logger.error(error_msg, extra={"stage": "error", "event_id": event_id, "trace_id": trace_id})
# Example: Log incident creation
def log_incident(incident_id, event_id, trace_id):
	logger.info("Incident created", extra={"stage": "incident_creation", "incident_id": incident_id, "event_id": event_id, "trace_id": trace_id})
