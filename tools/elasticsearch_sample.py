# Example: Index log/event to Elasticsearch
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index a log/event
es.index(index="aire-logs", document={
    "timestamp": "2026-02-26T22:57:00",
    "trace_id": "your-trace-id",
    "event_id": "your-event-id",
    "message": "Something happened",
    "level": "INFO"
})
