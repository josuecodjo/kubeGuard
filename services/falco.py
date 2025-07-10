import requests
import pandas as pd
import json
from datetime import datetime

def fetch_falco_logs(loki_url: str, query: str):
    response = requests.get(f"{loki_url}/loki/api/v1/query_range", params={
        "query": query,
        "limit": 100,
        "direction": "BACKWARD"
    })
    response.raise_for_status()
    data = response.json()

    logs = []
    for stream in data.get("data", {}).get("result", []):
        for value in stream["values"]:
            timestamp = datetime.utcfromtimestamp(int(value[0]) / 1e9)
            try:
                log_data = json.loads(value[1])
                logs.append({
                    "time": timestamp,
                    "priority": log_data.get("priority", "N/A"),
                    "rule": log_data.get("rule", ""),
                    "output": log_data.get("output", ""),
                    "source": log_data.get("source", ""),
                })
            except json.JSONDecodeError:
                logs.append({"time": timestamp, "output": value[1], "priority": "unknown", "rule": "n/a", "source": "unknown"})

    return pd.DataFrame(logs)
