import requests
import pandas as pd

def get_policy_violations(base_url="http://localhost:8080"):
    resp = requests.get(f"{base_url}/api/policies/violation")
    resp.raise_for_status()
    violations = resp.json().get("results", [])
    df = pd.DataFrame(violations)
    return df
