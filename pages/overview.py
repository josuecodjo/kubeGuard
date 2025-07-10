import streamlit as st
import plotly.express as px
from services.falco import fetch_falco_logs
from services.kyverno import get_policy_violations
from services.kubescape import run_kubescape, parse_kubescape_summary_controls
import time

st.set_page_config(page_title="KubeShield Overview", layout="wide")
st.title("📊 Unified KubeShield Security Dashboard")

# --- Auto-refresh toggle
st.sidebar.subheader("⏱️ Auto-Refresh")
if "refresh" not in st.session_state:
    st.session_state.refresh = False

start = st.sidebar.button("▶️ Start Auto-Refresh")
stop = st.sidebar.button("⏹️ Stop Refresh")
interval = st.sidebar.slider("Interval (sec)", 5, 120, 30)

if start:
    st.session_state.refresh = True
if stop:
    st.session_state.refresh = False


# --- Sidebar configuration
with st.sidebar:
    st.subheader("⚙️ Configuration")
    loki_url = st.text_input("Loki URL", "http://localhost:3100")
    loki_query = st.text_input("Loki Query", '{job="falco"}')
    kyverno_url = st.text_input("Policy Reporter API", "http://localhost:8080")

# --- Data Fetching
st.markdown("### 🔄 Fetching Data")

while True:
    # Falco logs
    falco_df = fetch_falco_logs(loki_url, loki_query)
    # Kyverno violations
    kyverno_df = get_policy_violations(kyverno_url)

    # Kubescape scan
    kubescape_data = run_kubescape()
    if kubescape_data:
        ks_df = parse_kubescape_summary_controls(kubescape_data)
        ks_score = kubescape_data.get("summaryDetails", {}).get("complianceScore", 0)
    else:
        ks_df = None
        ks_score = 0

    # --- KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🔔 Falco Alerts", len(falco_df))
    col2.metric("📜 Kyverno Violations", len(kyverno_df))
    col3.metric("🛡️ Kubescape Compliance Score", round(ks_score, 2))

    st.markdown("---")

    # --- Falco Visualization
    if not falco_df.empty:
        st.subheader("🚨 Falco Alerts by Severity")
        fig = px.histogram(falco_df, x="priority", color="priority", title="Falco Alert Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Falco alerts available.")

    # --- Kyverno Visualization
    if not kyverno_df.empty:
        st.subheader("📋 Kyverno Violations by Severity")
        fig = px.pie(kyverno_df, names="severity", title="Kyverno Severity Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Kyverno violations available.")

    # --- Kubescape Visualization
    if ks_df is not None and not ks_df.empty:
        failed_df = ks_df[ks_df["Status"].str.lower() == "failed"]
        if not failed_df.empty:
            st.subheader("❌ Kubescape Failed Controls (Top Severity)")
            chart = px.bar(
                failed_df.sort_values("Score", ascending=False).head(10),
                x="Control Name",
                y="Score",
                color="Category",
                title="Top Failed Controls",
                labels={"Score": "Severity Score"}
            )
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.success("✅ No failed controls detected by Kubescape.")
    else:
        st.info("No Kubescape data available.")

    if not st.session_state.refresh:
        break

    st.info(f"⏳ Refreshing again in {interval} seconds... (press Stop to cancel)")
    time.sleep(interval)
    st.experimental_rerun()