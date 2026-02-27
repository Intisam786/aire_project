import json
import os

def append_incident(incident, filename="data/incidents.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
    with open(filename, "r+") as f:
        data = json.load(f)
        data.append(incident)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
