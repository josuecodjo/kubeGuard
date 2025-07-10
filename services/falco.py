import requests
import pandas as pd

def fetch_falco_logs(loki_url: str, query: str):
    response = requests.get(f"{loki_url}/loki/api/v1/query_range", params={
        "query": query,
        "limit": 100,
        "direction": "BACKWARD"
    })
    response.raise_for_status()
    data = response.json()
    logs = [
        {
            "time": stream["values"][0][0],
            "log": stream["values"][0][1]
        }
        for stream in data.get("data", {}).get("result", [])
    ]
    return pd.DataFrame(logs)
