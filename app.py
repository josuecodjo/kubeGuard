import streamlit as st
from services.auth import setup_auth

# authenticator = setup_auth()

# name, auth_status, username = authenticator.login("Login", "main")

# if auth_status is False:
#     st.error("❌ Invalid credentials")
#     st.stop()
# elif auth_status is None:
#     st.warning("👤 Please enter your credentials")
#     st.stop()

# authenticator.logout("Logout", "sidebar")
# st.sidebar.success(f"✅ Logged in as {name}")

st.set_page_config(page_title="KubeShield Dashboard", layout="wide")
st.title("🛡️ KubeGuard: Unified K8s Security Dashboard")

st.markdown("""
Welcome to **KubeShield**, your single-pane dashboard for:
- Real-time Falco threat detection
- Kyverno policy violations
- Kubescape posture scans
""")
