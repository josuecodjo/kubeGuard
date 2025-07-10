import streamlit as st

st.set_page_config(page_title="KubeShield Dashboard", layout="wide")
st.title("🛡️ KubeGuard: Unified K8s Security Dashboard")

st.markdown("""
Welcome to **KubeShield**, your single-pane dashboard for:
- Real-time Falco threat detection
- Kyverno policy violations
- Kubescape posture scans
""")
