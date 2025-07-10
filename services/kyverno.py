import requests
import pandas as pd

def get_policy_violations(base_url="http://localhost:8080"):
    resp = requests.get(f"{base_url}/api/policies/violation")
    resp.raise_for_status()
    results = resp.json().get("results", [])

    records = []
    for r in results:
        records.append({
            "policy": r.get("policy", "N/A"),
            "rule": r.get("rule", "N/A"),
            "resourceKind": r.get("resource", {}).get("kind", "N/A"),
            "resourceName": r.get("resource", {}).get("name", "N/A"),
            "namespace": r.get("resource", {}).get("namespace", "default"),
            "message": r.get("message", ""),
            "severity": r.get("severity", "medium"),
            "status": r.get("status", "fail"),
            "timestamp": r.get("timestamp", "N/A")
        })

    return pd.DataFrame(records)
