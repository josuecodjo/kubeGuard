import json
import subprocess
import pandas as pd
import streamlit as st

def run_kubescape():
    try:
        result = subprocess.run(
            ['kubescape', 'scan', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error("Failed to run Kubescape. Make sure it's installed and configured.")
        return None

def parse_kubescape_summary_controls(data):
    controls = []
    raw_controls = data.get("summaryDetails", {}).get("controls", {})

    for ctrl_id, ctrl in raw_controls.items():
        rc = ctrl.get("ResourceCounters", {})
        controls.append({
            "Control ID": ctrl.get("controlID", ctrl_id),
            "Control Name": ctrl.get("name", "Unnamed"),
            "Status": ctrl.get("status", "unknown"),
            "Score": ctrl.get("score", 0),
            "Compliance Score": ctrl.get("complianceScore", 0),
            "Passed": rc.get("passedResources", 0),
            "Failed": rc.get("failedResources", 0),
            "Skipped": rc.get("skippedResources", 0),
            "Excluded": rc.get("excludedResources", 0),
            "Category": ctrl.get("category", {}).get("name", "Unknown")
        })
    return pd.DataFrame(controls)