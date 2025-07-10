import streamlit as st
import pandas as pd
import json
import plotly.express as px
import threading

from services.kubescape import run_kubescape, parse_kubescape_summary_controls

st.header("🔐 Kubescape Compliance Dashboard")

# --- User Options
# namespace = st.text_input("Kubernetes Namespace", "default")
framework = st.selectbox("Security Framework", ["nsa", "mitre", "cis", "all"])
save_output = st.checkbox("💾 Save report to local file", value=True)

if st.button("▶️ Run Kubescape Scan"):
    st.info("Running Kubescape...")
    data = run_kubescape(framework=framework)
    if data:
        df = parse_kubescape_summary_controls(data)

        st.subheader("📋 Control Summary")
        st.dataframe(df)

        st.subheader("📊 Failed Controls by Severity")
        failed_df = df[df["Status"].str.lower() == "failed"]
        if not failed_df.empty:
            fig = px.bar(
                failed_df.sort_values("Score", ascending=False).head(10),
                x="Control Name",
                y="Score",
                color="Category",
                title="Top Failed Controls",
                labels={"Score": "Severity Score"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No failed controls detected.")
