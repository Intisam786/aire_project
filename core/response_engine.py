
from utility.logger import get_logger
logger = get_logger()

def simulate_disable_account(user, trace_id=None):
    if trace_id is None:
        trace_id = "N/A"
    logger.info(
        "Simulated account disable",
        extra={
            "trace_id": trace_id,
            "stage": "response_execution",
            "user": user
        }
    )
    return True
