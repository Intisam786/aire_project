import logging
import sys
import json
from datetime import datetime
from utility.elasticsearch_logger import ElasticsearchLogHandler

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log_record.update(record.extra)
        return json.dumps(log_record)

def get_logger(name="AIRE"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        # Add Elasticsearch handler
        es_handler = ElasticsearchLogHandler()
        logger.addHandler(es_handler)
    return logger
