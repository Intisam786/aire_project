import logging
from elasticsearch import Elasticsearch
from datetime import datetime

class ElasticsearchLogHandler(logging.Handler):
    def __init__(self, es_host="http://localhost:9200", index="aire-logs"):
        super().__init__()
        self.es = Elasticsearch(es_host)
        self.index = index

    def emit(self, record):
        log_entry = self.format_record(record)
        try:
            self.es.index(index=self.index, document=log_entry)
        except Exception as e:
            # Optionally print or log errors to console/file
            print(f"Failed to index log to Elasticsearch: {e}")

    def format_record(self, record):
        # Start with the default fields
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        # Add all extra fields from the record (including agent, stage, etc.)
        for key, value in record.__dict__.items():
            if key not in log_entry and key not in ("args", "msg", "exc_info", "exc_text", "stack_info", "lineno", "pathname", "filename", "module", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process", "levelno", "name"):
                log_entry[key] = value
        return log_entry
